import os
import streamlit as st
from openai import OpenAI
import tempfile
from dotenv import load_dotenv

# Load environment variables from .env file (if it exists)
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="OpenAI Chat Interface",
    page_icon="💬",
    layout="wide",
)

# Check for API key
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    st.error("No OpenAI API key found. Please add your API key to the .env file.")
    st.stop()

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Function to get available models
def get_available_models():
    try:
        response = client.models.list()
        models = [model.id for model in response.data]
        # Filter for chat models and sort by newest first
        chat_models = [m for m in models if any(prefix in m for prefix in ["gpt-", "claude-"])]
        return sorted(chat_models, reverse=True)
    except Exception as e:
        st.error(f"Error fetching models: {e}")
        return ["gpt-4o", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"]

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Title
st.title("OpenAI Chat Interface")

# Sidebar for model selection and parameters
with st.sidebar:
    st.header("Settings")
    
    # API Key input (for convenience, but not recommended for production)
    with st.expander("API Key Settings", expanded=False):
        current_api_key = st.text_input("OpenAI API Key", value="", type="password", 
                                        help="Enter your OpenAI API key. For security, it's better to use the .env file.")
        if current_api_key and current_api_key != api_key:
            client = OpenAI(api_key=current_api_key)
            st.success("API key updated for this session")
    
    # Model selection
    models = get_available_models()
    selected_model = st.selectbox(
        "Select Model",
        options=models,
        index=0 if "gpt-4o" in models else 0,
    )
    
    # Temperature slider
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Higher values make output more random, lower values make it more deterministic"
    )
    
    # Max tokens slider
    max_tokens = st.slider(
        "Max Tokens",
        min_value=100,
        max_value=4096,
        value=1024,
        step=100,
        help="Maximum number of tokens to generate"
    )
    
    # Top P slider
    top_p = st.slider(
        "Top P",
        min_value=0.1,
        max_value=1.0,
        value=1.0,
        step=0.1,
        help="Nucleus sampling parameter"
    )
    
    # Frequency penalty slider
    frequency_penalty = st.slider(
        "Frequency Penalty",
        min_value=-2.0,
        max_value=2.0,
        value=0.0,
        step=0.1,
        help="Positive values penalize tokens based on their frequency in the text"
    )
    
    # Presence penalty slider
    presence_penalty = st.slider(
        "Presence Penalty",
        min_value=-2.0,
        max_value=2.0,
        value=0.0,
        step=0.1,
        help="Positive values penalize tokens that have already appeared in the text"
    )
    
    # File upload
    uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf", "docx", "csv", "json", "py", "js", "html", "css"])
    
    if uploaded_file:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
        
        st.success(f"File uploaded: {uploaded_file.name}")
        
        # Option to include file content in the prompt
        include_file = st.checkbox("Include file content in the prompt", value=True)
        
        if include_file:
            try:
                with open(tmp_path, "r") as f:
                    file_content = f.read()
                st.session_state.file_content = file_content
                st.info(f"File content loaded ({len(file_content)} characters)")
            except Exception as e:
                st.error(f"Error reading file: {e}")
                st.session_state.file_content = None
    else:
        st.session_state.file_content = None
    
    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.file_content = None
        st.experimental_rerun()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.write(user_input)
    
    # Prepare messages for API call
    messages_for_api = []
    
    # Add system message if file content is available
    if st.session_state.file_content:
        messages_for_api.append({
            "role": "system", 
            "content": f"The user has uploaded a file with the following content:\n\n{st.session_state.file_content}\n\nPlease consider this information when responding to their queries."
        })
    
    # Add chat history
    for message in st.session_state.messages:
        messages_for_api.append({"role": message["role"], "content": message["content"]})
    
    # Display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Make API call with streaming
            stream = client.chat.completions.create(
                model=selected_model,
                messages=messages_for_api,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                stream=True,
            )
            
            # Process streaming response
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.write(full_response + "▌")
            
            message_placeholder.write(full_response)
        except Exception as e:
            st.error(f"Error: {e}")
            full_response = f"I apologize, but an error occurred: {e}"
            message_placeholder.write(full_response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# Footer
st.markdown("---")
st.caption("Powered by OpenAI API • Built with Streamlit")