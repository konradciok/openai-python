import streamlit as st
from components.image_upload import image_upload
from components.description_form import description_form
from components.description_preview import description_preview
from utils.image_analyzer import analyze_image
from utils.description_generator import generate_description

def show():
    st.title("Fine Art Print Description Generator")
    
    # Introduction
    st.markdown("""
    Create compelling product descriptions for your fine art prints using AI.
    Upload an image of your artwork, add details, and get a professionally crafted description.
    """)
    
    # Step 1: Image Upload
    st.subheader("Step 1: Upload Artwork Image")
    uploaded_image = image_upload()
    
    # Process the uploaded image
    if uploaded_image is not None and "image_analysis" not in st.session_state:
        with st.spinner("Analyzing image..."):
            try:
                # Analyze the image using OpenAI Vision
                analysis_results = analyze_image(uploaded_image)
                
                # Store analysis in session state
                st.session_state.image_analysis = analysis_results
                
                # Pre-fill form fields based on image analysis if analysis_results is a dictionary
                if isinstance(analysis_results, dict):
                    if "detected_style" in analysis_results:
                        st.session_state.art_style = analysis_results["detected_style"]
                    if "detected_medium" in analysis_results:
                        st.session_state.medium = analysis_results["detected_medium"]
                    if "detected_colors" in analysis_results:
                        st.session_state.detected_colors = analysis_results["detected_colors"]
                    if "detected_subject" in analysis_results:
                        st.session_state.detected_subject = analysis_results["detected_subject"]
                    if "detected_mood" in analysis_results:
                        st.session_state.detected_mood = analysis_results["detected_mood"]
                    
                    st.success("Image analyzed successfully!")
                    st.rerun()
                else:
                    st.error("Failed to analyze image. Please try again.")
            except Exception as e:
                st.error(f"Error analyzing image: {str(e)}")
                st.session_state.image_analysis = {}
    
    # Create two columns for form and preview
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Step 2: Input Form
        st.subheader("Step 2: Add Details")
        
        # Show image analysis results if available
        if "image_analysis" in st.session_state and st.session_state.image_analysis is not None:
            with st.expander("Image Analysis Results", expanded=False):
                st.write("Our AI detected the following elements in your artwork:")
                
                analysis_data = st.session_state.image_analysis
                if isinstance(analysis_data, dict):
                    if "detected_style" in analysis_data:
                        st.write(f"**Style:** {analysis_data['detected_style']}")
                    if "detected_medium" in analysis_data:
                        st.write(f"**Medium:** {analysis_data['detected_medium']}")
                    if "detected_colors" in analysis_data:
                        st.write(f"**Color Palette:** {analysis_data['detected_colors']}")
                    if "detected_subject" in analysis_data:
                        st.write(f"**Subject:** {analysis_data['detected_subject']}")
                    if "detected_mood" in analysis_data:
                        st.write(f"**Mood:** {analysis_data['detected_mood']}")
                else:
                    st.write("No analysis data available yet.")
        
        # Display the form
        form_submitted = description_form()
        
        if form_submitted:
            # Generate description when form is submitted
            with st.spinner("Generating description..."):
                try:
                    # Combine image analysis with form data
                    image_data = st.session_state.get("image_analysis", {})
                    
                    # Get keywords if available
                    keywords = st.session_state.get("keywords", "")
                    
                    # Get tone and length preferences
                    tone = st.session_state.get("description_tone", "Professional")
                    length = st.session_state.get("description_length", 150)
                    
                    description = generate_description(
                        st.session_state.print_title,
                        st.session_state.artist_name,
                        st.session_state.art_style,
                        st.session_state.medium,
                        st.session_state.dimensions,
                        st.session_state.year_created,
                        st.session_state.additional_details,
                        image_data,
                        keywords,
                        tone,
                        length
                    )
                    
                    # Check if the description was generated successfully
                    if description and not description.startswith("Error generating description"):
                        st.session_state.current_description = description
                        st.success("Description generated successfully!")
                    else:
                        st.error(description)
                        # Use demo description as fallback
                        from utils.description_generator import demo_generate_description
                        fallback_description = demo_generate_description(
                            st.session_state.print_title,
                            st.session_state.artist_name,
                            st.session_state.art_style,
                            st.session_state.medium,
                            st.session_state.dimensions,
                            st.session_state.year_created,
                            st.session_state.additional_details,
                            image_data,
                            keywords,
                            tone,
                            length
                        )
                        st.session_state.current_description = fallback_description
                        st.warning("Using demo description as fallback. To use the AI-generated description, please add a valid OpenAI API key to your .env file.")
                except Exception as e:
                    st.error(f"Error generating description: {str(e)}")
                    st.session_state.current_description = f"An error occurred while generating the description. Please try again."
    
    with col2:
        # Step 3: Preview
        st.subheader("Step 3: Preview & Export")
        
        # Show the uploaded image
        if uploaded_image is not None:
            st.image(uploaded_image, caption="Uploaded Artwork", use_container_width=True)
        
        # Preview the generated description
        description_preview()