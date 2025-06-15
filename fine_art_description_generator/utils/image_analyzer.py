import base64
import os
import json
from io import BytesIO
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def encode_image(image_file):
    """
    Encode the image file to base64 for API submission  
    """
    # Read the file and convert to bytes
    image_bytes = image_file.getvalue()
    
    # Encode to base64
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    
    return base64_image

def analyze_image(image_file):
    """
    Analyze the uploaded image using OpenAI's Vision API
    
    Args:
        image_file: The uploaded image file
        
    Returns:
        dict: Analysis results including detected style, medium, colors, etc.
    """
    # First try to use the API, if it fails, use the demo function
    try:
        # Encode image to base64
        base64_image = encode_image(image_file)
        
        # Create the prompt for image analysis
        prompt = """
        Analyze this fine art print image in detail. Provide the following information:
        
        1. Detected art style (e.g., Abstract, Impressionism, Surrealism, etc.)
        2. Likely medium or print technique
        3. Dominant color palette (describe the main colors)
        4. Subject matter or content (what is depicted)
        5. Overall mood or emotional tone
        
        Format your response as a JSON object with the following keys:
        "detected_style", "detected_medium", "detected_colors", "detected_subject", "detected_mood"
        
        Be specific and descriptive, but keep each field concise (1-2 sentences maximum).
        """
        
        # Call OpenAI API with vision capabilities
        # Try with the current model name for vision
        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo",  # Try the current vision-capable model
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}",
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=500,
                response_format={"type": "json_object"}
            )
        except Exception as model_error:
            # If the first model fails, try with an alternative model
            print(f"First model attempt failed: {str(model_error)}")
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",  # Try alternative model
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64_image}",
                                        "detail": "high"
                                    }
                                }
                            ]
                        }
                    ],
                    max_tokens=500,
                    response_format={"type": "json_object"}
                )
            except Exception as alt_model_error:
                # If both models fail, raise the error to be caught by the outer try-except
                print(f"Alternative model attempt failed: {str(alt_model_error)}")
                raise alt_model_error
        
        # Extract and parse the JSON response
        analysis_text = response.choices[0].message.content
        analysis_data = json.loads(analysis_text)
        
        return analysis_data
    
    except Exception as e:
        # Log the error
        print(f"Error analyzing image: {str(e)}")
        
        # Use the demo function as a fallback
        print("Using demo analysis as fallback")
        return demo_analyze_image(image_file)

# Fallback function for demo purposes (when no API key is available)
def demo_analyze_image(image_file):
    """Generate sample analysis when API is not available"""
    return {
        "detected_style": "Abstract Expressionism",
        "detected_medium": "Giclée Print",
        "detected_colors": "Deep blues, vibrant reds, and golden accents on a neutral background",
        "detected_subject": "Non-representational composition with fluid forms suggesting movement and emotion",
        "detected_mood": "Contemplative and energetic, with a sense of dynamic tension"
    }