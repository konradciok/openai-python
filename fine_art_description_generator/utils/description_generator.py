import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_description(title, artist, style, medium, dimensions, year, additional_details, image_data=None, keywords=None, tone="Professional", length=150):
    """
    Generate a product description for a fine art print using OpenAI's API
    
    Args:
        title (str): Title of the print
        artist (str): Name of the artist
        style (str): Art style (e.g., Abstract, Impressionism)
        medium (str): Print medium (e.g., Giclée Print, Screen Print)
        dimensions (str): Dimensions of the print
        year (str): Year the artwork was created
        additional_details (str): Any additional details about the print
        image_data (dict): Optional data from image analysis
        keywords (str): Optional SEO keywords
        tone (str): Tone of the description (Professional, Casual, etc.)
        length (int): Target length of the description in words
        
    Returns:
        str: Generated product description
    """
    try:
        # Extract image analysis data if available
        image_analysis_text = ""
        if image_data and isinstance(image_data, dict):
            image_analysis_text = "Image Analysis Results:\n"
            for key, value in image_data.items():
                if key != "error" and value and not key.startswith("_"):  # Skip error messages and private fields
                    image_analysis_text += f"- {key.replace('detected_', '').capitalize()}: {value}\n"
        
        # Create a prompt for the AI
        prompt = f"""
        Create a compelling, SEO-friendly product description for a fine art print with the following details:
        
        Title: {title}
        Artist: {artist}
        Style: {style}
        Medium: {medium}
        Dimensions: {dimensions}
        Year: {year}
        Additional Details: {additional_details}
        
        {image_analysis_text}
        
        Tone: {tone}
        Target Length: Approximately {length} words
        SEO Keywords: {keywords if keywords else ""}
        
        The description should:
        1. Highlight the visual elements and emotional impact of the artwork
        2. Mention the quality of the print and materials
        3. Include details about the artist's technique or inspiration if relevant
        4. Use language that appeals to art collectors and enthusiasts
        5. Be written in a {tone.lower()} tone
        6. Include relevant keywords for SEO naturally
        7. Emphasize what makes this print special and worth purchasing
        
        Format the description as a cohesive paragraph that would be suitable for a Shopify product page.
        """
        
        # Try different models in case one fails
        try:
            # First try with GPT-4
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert art curator and copywriter specializing in fine art prints for e-commerce."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
        except Exception as model_error:
            print(f"First model attempt failed: {str(model_error)}")
            # If GPT-4 fails, try with GPT-3.5 Turbo
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an expert art curator and copywriter specializing in fine art prints for e-commerce."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1000,
                    temperature=0.7
                )
            except Exception as alt_model_error:
                print(f"Alternative model attempt failed: {str(alt_model_error)}")
                # If both models fail, use the demo function
                return demo_generate_description(title, artist, style, medium, dimensions, year, additional_details, image_data, keywords, tone, length)
        
        # Extract and return the generated description
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        # Log the error
        print(f"Error generating description: {str(e)}")
        
        # Use the demo function as a fallback
        print("Using demo description as fallback")
        return demo_generate_description(title, artist, style, medium, dimensions, year, additional_details, image_data, keywords, tone, length)


# Fallback function for demo purposes (when no API key is available)
def demo_generate_description(title, artist, style, medium, dimensions, year, additional_details, image_data=None, keywords=None, tone="Professional", length=150):
    """Generate a sample description when API is not available"""
    
    # Extract some image data if available
    colors = image_data.get("detected_colors", "vibrant") if image_data else "vibrant"
    subject = image_data.get("detected_subject", "composition") if image_data else "composition"
    mood = image_data.get("detected_mood", "captivating") if image_data else "captivating"
    
    return f"""
    "{title}" by {artist} ({year}) is a stunning {style.lower()} {medium.lower()} that captures the essence of contemporary fine art. Measuring {dimensions}, this limited edition print showcases the artist's masterful technique and unique artistic vision.
    
    The artwork features a {colors.lower()} palette that brings the {subject.lower()} to life, creating a {mood.lower()} visual experience that is both intellectually stimulating and aesthetically pleasing. Each print is produced using premium archival inks on museum-quality paper, ensuring exceptional color accuracy and longevity.
    
    {additional_details}
    
    Whether displayed in a modern living space, office, or gallery, this print makes a sophisticated statement and serves as a focal point for any room. A certificate of authenticity is included with each purchase, making this a valuable addition to any art collection.
    """