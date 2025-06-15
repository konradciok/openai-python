"""
data_analyzer.py
────────────────
Vision helper that returns **deterministic, slot-friendly JSON**
for downstream DescriptionBundle generation.

Key upgrades
------------
1.  Extract dominant colors locally (Pillow + numpy) → feed them to GPT
    so the model *confirms* rather than hallucinates.
2.  Tighter prompt:    • explicitly lists required keys
                       • hard word caps in parenthesis
                       • "respond ONLY with JSON".
3.  Output keys match the slot schema used by core.prompt_slots.
"""

from __future__ import annotations

import base64
import json
import os
from io import BytesIO
from pathlib import Path
from typing import Dict, List
import logging

import numpy as np
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image
from sklearn.cluster import KMeans

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# --------------------------------------------------------------------- #
# 1.  Setup
# --------------------------------------------------------------------- #

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --------------------------------------------------------------------- #
# 2.  Utility — local color extraction to anchor GPT
# --------------------------------------------------------------------- #


def _extract_dominant_colors(image: Image.Image, k: int = 3) -> List[Dict[str, str]]:
    """
    Return `k` dominant colors as simple dicts: {"hex": "#rrggbb"}
    """
    img = image.convert("RGB").resize((150, 150))  # speed
    data = np.array(img).reshape(-1, 3) / 255.0

    km = KMeans(n_clusters=k, n_init=8, random_state=42).fit(data)
    centroids = (km.cluster_centers_ * 255).astype(int)

    def to_hex(rgb) -> str:
        return "#{:02x}{:02x}{:02x}".format(*rgb)

    return [{"hex": to_hex(c)} for c in centroids]


def _color_blocks_md(colors: List[Dict[str, str]]) -> str:
    """
    Turn color hex codes into a mini-markdown table for the GPT prompt.
    """
    rows = [f"| {c['hex']} |  |" for c in colors]
    header = "| HEX | swatch |\n|-----|--------|"
    return header + "\n" + "\n".join(rows)


# --------------------------------------------------------------------- #
# 3.  OpenAI Vision call
# --------------------------------------------------------------------- #


def _encode_image(image: Image.Image) -> str:
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def analyze_image(image_file) -> Dict[str, object]:
    """
    Main entry point — accepts a Streamlit `UploadedFile` or any file-like.
    Always returns JSON with keys expected by DescriptionBundle.visual_analysis.
    """
    try:
        pil_image = Image.open(image_file).convert("RGBA")
        logging.debug(f"Image loaded successfully: {image_file.name}")
    except Exception as err:  # pylint: disable=broad-except
        logging.error(f"Error loading image: {err}")
        raise RuntimeError("Could not load image") from err

    # ---------- Local color anchor ----------------------------------- #
    dom_colors = _extract_dominant_colors(pil_image, k=3)
    logging.debug(f"Dominant colors extracted: {dom_colors}")
    colors_prompt_md = _color_blocks_md(dom_colors)

    # ---------- Build vision prompt ---------------------------------- #
    sys_prompt = f"""
You are a senior e-commerce copywriting assistant with expertise in SEO 2025, fine art prints, and Shopify optimization. Your task is to create product descriptions that are emotionally engaging, SEO-optimized, conversion-focused, and structured for mobile-friendly Shopify stores. Descriptions must follow keyword hierarchy rules, structure guidelines, and include both storytelling and technical specifications..  Return a *single JSON object* with these keys:
  "style"           (≤ 12 words)
  "medium"          (≤ 5 words)
  "dominant_colors" (use supplied hex + one-word names)
  "key_shapes"      (array of ≤10 short noun phrases)
  "mood"            (≤ 8 words)
  "has_signature"   (true/false)

Use the format below EXACTLY:

{{
  "style": "...",
  "medium": "...",
  "dominant_colors": [{{"name": "...", "hex": "#......"}}, ...],
  "key_shapes": ["...", "..."],
  "mood": "...",
  "has_signature": true
}}

**Respond ONLY with JSON.**

These are the pre-extracted dominant colors — keep hex codes unchanged:

{colors_prompt_md}
""".strip()

    vision_msg = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": sys_prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{_encode_image(pil_image)}",
                        "detail": "high",
                    },
                },
            ],
        }
    ]

    # ---------- Call the model -------------------------------------- #
    logging.debug("Sending vision prompt to OpenAI API")
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=vision_msg,
        max_tokens=400,
        response_format={"type": "json_object"},
    )

    try:
        result = json.loads(resp.choices[0].message.content)
        logging.debug(f"API response parsed successfully: {result}")
        return result
    except json.JSONDecodeError as err:
        logging.error(f"Error parsing API response: {err}")
        raise RuntimeError("Vision model did not return valid JSON") from err


# --------------------------------------------------------------------- #
# 4.  DEMO fallback (no API key) -------------------------------------- #


def demo_analyze_image(image_file) -> Dict[str, object]:  # noqa: D401
    """Static sample for offline dev."""
    return {
        "style": "Abstract organic minimalism",
        "medium": "Giclée fine-art print",
        "dominant_colors": [
            {"name": "cerulean", "hex": "#2994d9"},
            {"name": "sand beige", "hex": "#d8c4a4"},
            {"name": "navy ink", "hex": "#14233c"},
        ],
        "key_shapes": ["concentric loop", "ink droplet"],
        "mood": "Calming",
        "has_signature": True,
    }
