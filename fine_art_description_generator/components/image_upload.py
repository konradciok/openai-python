import streamlit as st
import io
from PIL import Image

def image_upload():
    """
    Component for uploading and displaying artwork images
    
    Returns:
        The uploaded image file if successful, None otherwise
    """
    # File uploader for artwork images
    uploaded_file = st.file_uploader(
        "Upload an image of your fine art print", 
        type=["jpg", "jpeg", "png", "webp"],
        help="Upload a clear, high-quality image of your artwork"
    )
    
    if uploaded_file is not None:
        try:
            # Store the image in session state
            if "uploaded_image" not in st.session_state or st.session_state.uploaded_image != uploaded_file:
                # Reset image analysis when a new image is uploaded
                if "image_analysis" in st.session_state:
                    del st.session_state.image_analysis
                
                # Store the new image
                st.session_state.uploaded_image = uploaded_file
                
                # Display image information
                try:
                    image = Image.open(uploaded_file)
                    
                    # Check if the image is valid
                    image.verify()  # Verify that it's an image
                    
                    # Need to reopen after verify
                    uploaded_file.seek(0)
                    image = Image.open(uploaded_file)
                    
                    file_details = {
                        "Filename": uploaded_file.name,
                        "File size": f"{uploaded_file.size / 1024:.1f} KB",
                        "Image dimensions": f"{image.width} x {image.height} px"
                    }
                    
                    with st.expander("Image Details", expanded=False):
                        for key, value in file_details.items():
                            st.write(f"**{key}:** {value}")
                except Exception as img_error:
                    st.error(f"Error processing image: {str(img_error)}")
                    st.warning("Please try uploading a different image file.")
                    return None
            
            # Reset file position for further processing
            uploaded_file.seek(0)
            return uploaded_file
        except Exception as e:
            st.error(f"Error handling uploaded file: {str(e)}")
            return None
    
    # If no image is uploaded yet
    if "uploaded_image" not in st.session_state:
        st.info("Please upload an image of your artwork to begin.")
    
    return None