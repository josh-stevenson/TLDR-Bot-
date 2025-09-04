import streamlit as st
import requests
import pypdf
import io

# --- Page Configuration ---
st.set_page_config(
    page_title="Private LLM Chat",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Private LLM Interaction Hub")

# --- Helper Functions ---

def extract_text_from_pdf(pdf_file):
    """Extracts text from an uploaded PDF file."""
    try:
        pdf_reader = pypdf.PdfReader(io.BytesIO(pdf_file.read()))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        st.error(f"Error reading PDF file: {e}")
        return None

def get_llm_response(prompt_text):
    """
    Sends a prompt to the LLM and gets a response.
    Loads credentials securely from st.secrets.
    """
    # --- Load credentials and config from the secrets file ---
    # This is the key change: No more hardcoded values.
    try:
        api_key = st.secrets["API_KEY"]
        api_url = st.secrets["API_URL"]
        model_name = st.secrets["MODEL_NAME"]
    except KeyError as e:
        st.error(f"Missing credential in secrets.toml: {e}. Please check your configuration.")
        return None

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            *st.session_state.messages, # Include past conversation
            {"role": "user", "content": prompt_text}
        ]
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=120)
        response.raise_for_status() # Raises an error for bad status codes
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Error communicating with the API: {e}"
    except (KeyError, IndexError) as e:
        return f"Error parsing API response: {e}. Response: {response.text}"

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- UI Components ---

# Display existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Sidebar for Controls & File Upload
with st.sidebar:
    st.header("Document Upload")
    uploaded_file = st.file_uploader(
        "Upload a PDF for context", 
        type=['pdf']
    )

# User Input at the bottom
prompt = st.chat_input("Ask a question...")

# --- Main Logic ---
if prompt:
    # 1. Handle document context if a file is uploaded
    document_context = ""
    if uploaded_file is not None:
        # Avoid reprocessing the file on every message
        if "doc_text" not in st.session_state or st.session_state.uploaded_file_name != uploaded_file.name:
            with st.spinner("Processing document..."):
                st.session_state.doc_text = extract_text_from_pdf(uploaded_file)
                st.session_state.uploaded_file_name = uploaded_file.name
        
        if st.session_state.doc_text:
            document_context = f"--- DOCUMENT CONTEXT ---\n{st.session_state.doc_text}\n--- END CONTEXT ---"
    
    # Combine context and prompt
    full_prompt = f"{document_context}\n\nUser Question: {prompt}".strip()
    
    # 2. Add user message to chat history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # 3. Get LLM response and display it
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # The function call is now simpler
            response_text = get_llm_response(full_prompt)
            if response_text:
                st.markdown(response_text)
                # 4. Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response_text})

