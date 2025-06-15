import streamlit as st

def initialize_session_state():
    """
    Initialize session state variables if they don't exist
    """
    # Description state
    if "current_description" not in st.session_state:
        st.session_state.current_description = ""
    
    # Image state
    if "uploaded_image" not in st.session_state:
        st.session_state.uploaded_image = None
    
    if "image_analysis" not in st.session_state:
        st.session_state.image_analysis = None
    
    # Form fields
    default_fields = {
        "print_title": "",
        "artist_name": "",
        "art_style": "Abstract",
        "medium": "Giclée Print",
        "dimensions": "",
        "year_created": "",
        "description_tone": "Professional",
        "description_length": 150,
        "additional_details": "",
        "keywords": ""
    }
    
    # Initialize form fields if they don't exist
    for field, default_value in default_fields.items():
        if field not in st.session_state:
            st.session_state[field] = default_value
    
    # Add a reset function to session state
    if "reset_app" not in st.session_state:
        st.session_state.reset_app = reset_app

def reset_app():
    """
    Reset all session state variables to their default values
    """
    # List of keys to keep (don't reset)
    keys_to_keep = []
    
    # Get all keys in session state
    all_keys = list(st.session_state.keys())
    
    # Remove all keys except those in keys_to_keep
    for key in all_keys:
        if key not in keys_to_keep:
            del st.session_state[key]
    
    # Re-initialize session state
    initialize_session_state()