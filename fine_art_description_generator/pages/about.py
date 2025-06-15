import streamlit as st

def show():
    st.title("About This App")
    
    st.markdown("""
    ## Fine Art Print Description Generator
    
    This application helps fine art print sellers create professional, compelling product 
    descriptions for their Shopify e-commerce store using AI image analysis and natural 
    language generation.
    
    ### How It Works
    
    1. **Upload an image** of your fine art print
    2. Our AI analyzes the image to detect style, medium, colors, subject, and mood
    3. **Add additional details** about your print (title, artist, dimensions, etc.)
    4. Our AI generates a tailored description combining visual analysis with your input
    5. **Edit the description** if needed
    6. Copy or download the final text to use in your Shopify store
    
    ### Technology
    
    This application uses:
    - OpenAI's Vision API for image analysis
    - OpenAI's GPT models for natural language description generation
    - Streamlit for the user interface
    
    ### Benefits
    
    - Save time writing product descriptions
    - Create consistent, professional copy
    - Highlight the unique visual aspects of each print
    - Improve SEO with well-crafted descriptions
    - Ensure descriptions accurately reflect the artwork
    
    ### Privacy
    
    Uploaded images are processed for analysis but not stored permanently.
    Your data is used only for generating descriptions and is not shared with third parties.
    
    ### Contact
    
    For support or feedback, please contact us at support@example.com
    """)