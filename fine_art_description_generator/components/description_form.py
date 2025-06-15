import streamlit as st
import re

# ────────────────────────────────────────────────────────────── #
# Helper – derive title from uploaded filename
# Example "Unda_01_A3.jpg" → "Unda 01"
# Make sure you set st.session_state.uploaded_file_name
# right after the upload widget.
# ────────────────────────────────────────────────────────────── #
def _derive_title(filename: str) -> str:
    stem = filename.split(".")[0]                 # remove extension
    word_num = "_".join(stem.split("_")[:2])      # keep word + number
    return re.sub(r"_", " ", word_num).strip().title()


# ────────────────────────────────────────────────────────────── #
# Main form
# ────────────────────────────────────────────────────────────── #
def description_form() -> bool:
    """
    Lean print-metadata form reflecting new hard-coded business rules.
    Returns True when the “Generate Description” button is pressed.
    """
    with st.form(key="print_details_form"):
        st.markdown("### Print Metadata")

        # ─── 1 · Title derived from filename ──────────────────────── #
        file_name = st.session_state.get("uploaded_file_name", "Untitled_01.jpg")
        title = _derive_title(file_name)
        st.session_state.print_title = title
        st.text_input("Print Title", value=title, disabled=True)

        # ─── 2 · Hard-coded fields ───────────────────────────────── #
        st.session_state.artist_name = "Anna Ciok"
        st.text_input("Artist Name", value="Anna Ciok", disabled=True)

        st.session_state.art_style = "Watercolor"
        st.text_input("Art Style", value="Watercolor", disabled=True)

        st.session_state.medium = "paper"
        st.text_input("Print Medium", value="paper", disabled=True)

        st.session_state.dimensions = "multiple sizes available"
        st.text_input("Dimensions", value="multiple sizes available", disabled=True)

        st.session_state.year_created = "2025"
        st.text_input("Year Created", value="2025", disabled=True)

        # ─── 3 · Tone selector (SEO vs Shopify) ───────────────────── #
        tone = st.radio(
            "Description Tone",
            options=["SEO", "Shopify Product Page"],
            index=1,
            horizontal=True,
        )
        st.session_state.description_tone = tone

        # ─── 4 · SEO keywords only when tone == SEO ──────────────── #
        if tone == "SEO":
            st.session_state.keywords = st.text_input(
                "SEO Keywords (comma-separated)",
                value=st.session_state.get("keywords", ""),
                placeholder="e.g., abstract art, watercolor print, blue wall decor",
            )
        else:
            st.session_state.keywords = ""  # ignored downstream

        # ─── 5 · Submit ──────────────────────────────────────────── #
        submitted = st.form_submit_button("Generate Description")
        return submitted
