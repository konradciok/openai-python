import streamlit as st
from pages import home, about
from utils.session_state import initialize_session_state

def main():
    # Set page configuration
    st.set_page_config(
        page_title="Fine Art Description Generator",
        page_icon="🖼️",
        layout="centered",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Apply custom CSS
    with open("styles/main.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("Fine Art Description Generator")
    page = st.sidebar.radio("Navigation", ["Home", "About"])
    
    # Display the selected page
    if page == "Home":
        home.show()
    elif page == "About":
        about.show()

if __name__ == "__main__":
    main()