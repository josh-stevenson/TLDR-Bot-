import streamlit as st
import requests
import pypdf
import io

# --- Page Configuration ---
st.set_page_config(
    page_title="GPT-OSS-120b Chat",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 TLDR Bot with GPT-OSS-120b")

# --- Session State Initialization ---
# This is crucial to keep track of the chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display existing messages ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Sidebar for Controls & File Upload Widget---
with st.sidebar:
    st.header("Controls")
    uploaded_file = st.file_uploader(
        "Upload a document (PDF)", 
        type=['pdf']
    )
    # You can add other controls here, like temperature sliders etc.

# --- User Input at the bottom ---
prompt = st.chat_input("What would you like to ask your document?")

## Document Processing - extracts texts from PDF Files.

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
    
## API Communitcation Function ##
## This funtion calls GPT-OSS-120b endpoint

def get_llm_response(prompt_text, api_key="[YOUR_API_KEY_HERE"):
    """Sends a prompt to the LLM and gets a response."""
    api_url = "https://[YOUR_URL_HERE]/api/v1/chat/completions" # Replace with actual endpoint
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Construct the payload based on the API's requirements
    # This usually includes the model name and the message history
    payload = {
        "model": "[MODEL_ENDPOINT_NAME_HERE",
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
        with st.spinner("Thinking... 🤔"):
            response_text = get_llm_response(full_prompt)
            st.markdown(response_text)
            
    # 4. Add assistant response to chat history

    st.session_state.messages.append({"role": "assistant", "content": response_text})
