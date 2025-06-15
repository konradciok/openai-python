import streamlit as st

def description_form():
    """
    Renders the form for collecting print details and returns True if submitted
    """
    with st.form(key="print_details_form"):
        st.markdown("Enter details about your fine art print:")
        
        # Basic print information
        st.session_state.print_title = st.text_input(
            "Print Title", 
            value=st.session_state.get("print_title", ""),
            placeholder="e.g., Sunset Over Mountains"
        )
        
        st.session_state.artist_name = st.text_input(
            "Artist Name", 
            value=st.session_state.get("artist_name", ""),
            placeholder="e.g., Jane Smith"
        )
        
        # Art style and medium
        style_options = [
            "Abstract", "Impressionism", "Expressionism", "Minimalism", 
            "Surrealism", "Realism", "Pop Art", "Photography", "Digital Art", "Other"
        ]
        
        # Use detected style from image analysis if available
        default_style_index = 0
        if "art_style" in st.session_state and st.session_state.art_style in style_options:
            default_style_index = style_options.index(st.session_state.art_style)
        
        st.session_state.art_style = st.selectbox(
            "Art Style", 
            options=style_options,
            index=default_style_index
        )
        
        medium_options = [
            "Giclée Print", "Screen Print", "Lithograph", "Etching", 
            "Woodcut", "Digital Print", "Monotype", "Photograph", "Mixed Media", "Other"
        ]
        
        # Use detected medium from image analysis if available
        default_medium_index = 0
        if "medium" in st.session_state and st.session_state.medium in medium_options:
            default_medium_index = medium_options.index(st.session_state.medium)
        
        st.session_state.medium = st.selectbox(
            "Print Medium", 
            options=medium_options,
            index=default_medium_index
        )
        
        # Additional details
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.dimensions = st.text_input(
                "Dimensions (inches/cm)", 
                value=st.session_state.get("dimensions", ""),
                placeholder="e.g., 18 x 24 inches"
            )
        
        with col2:
            st.session_state.year_created = st.text_input(
                "Year Created", 
                value=st.session_state.get("year_created", ""),
                placeholder="e.g., 2023"
            )
        
        # Description tone and length preferences
        tone_options = ["Professional", "Casual", "Poetic", "Academic", "Minimalist"]
        st.session_state.description_tone = st.select_slider(
            "Description Tone",
            options=tone_options,
            value=st.session_state.get("description_tone", "Professional")
        )
        
        st.session_state.description_length = st.slider(
            "Description Length (words)",
            min_value=50,
            max_value=300,
            value=st.session_state.get("description_length", 150),
            step=25
        )
        
        st.session_state.additional_details = st.text_area(
            "Additional Details (optional)", 
            value=st.session_state.get("additional_details", ""),
            placeholder="Paper type, edition size, special techniques, inspiration, etc.",
            height=100
        )
        
        # Keywords for SEO
        st.session_state.keywords = st.text_input(
            "SEO Keywords (optional, comma-separated)",
            value=st.session_state.get("keywords", ""),
            placeholder="e.g., abstract art, modern print, blue, minimalist"
        )
        
        # Submit button
        submitted = st.form_submit_button("Generate Description")
        
        return submitted