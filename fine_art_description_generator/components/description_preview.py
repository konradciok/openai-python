import streamlit as st

def description_preview():
    """
    Renders the preview of the generated description with editing capabilities
    """
    # Check if a description exists
    if "current_description" in st.session_state and st.session_state.current_description:
        # Container for the preview with styling
        with st.container():
            st.markdown("##### Generated Description")
            
            # Allow editing the generated description
            edited_description = st.text_area(
                "Edit Description",
                value=st.session_state.current_description,
                height=300,
                label_visibility="collapsed"
            )
            
            # Update the description if edited
            if edited_description != st.session_state.current_description:
                st.session_state.current_description = edited_description
            
            # Export options in columns
            col1, col2 = st.columns(2)
            
            with col1:
                # Copy button
                if st.button("Copy to Clipboard"):
                    st.code(st.session_state.current_description)
                    st.success("Description copied to clipboard! (Use Ctrl+C or Cmd+C)")
            
            with col2:
                # Download button
                st.download_button(
                    label="Download as Text",
                    data=st.session_state.current_description,
                    file_name=f"{st.session_state.get('print_title', 'art_print').replace(' ', '_').lower()}_description.txt",
                    mime="text/plain"
                )
            
            # Shopify integration hint
            with st.expander("How to use in Shopify", expanded=False):
                st.markdown("""
                1. Copy the generated description
                2. In your Shopify admin, go to Products > Add/Edit product
                3. Paste the description in the "Description" field
                4. Save your product
                """)
    else:
        # Placeholder when no description is generated yet
        st.info("Your generated description will appear here after you upload an image and submit the form.")
        st.session_state.current_description = ""