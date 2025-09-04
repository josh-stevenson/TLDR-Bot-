Private LLM Chat Interface
This repository contains a simple yet powerful front-end application built with Streamlit to interact with a privately hosted Large Language Model (LLM). It provides a user-friendly chat interface that allows for direct prompting and document uploads for Retrieval-Augmented Generation (RAG).

## Why Host Your Own LLM?
Using public LLM APIs from providers like OpenAI, Google, or Anthropic is convenient, but it introduces significant risks and limitations. Hosting your own model, like the one this application is designed for, provides critical advantages for any serious enterprise.

### Data Privacy & Security
When you send data to a public API, it leaves your secure infrastructure. This data can be logged, stored, and sometimes even used to train future versions of the model. For any organization handling proprietary information, customer data, or sensitive internal documents, this is an unacceptable security risk. By hosting the model privately, your data never leaves your control.

### Compliance
Industries with strict regulatory requirements—such as healthcare (HIPAA), finance (GLBA, PCI DSS), or any entity dealing with European user data (GDPR)—must guarantee data residency and processing controls. A privately hosted LLM is often the only way to use this technology while remaining compliant.

### Cost Control & Predictability
Public API costs are typically usage-based, billed per token. For applications with high or unpredictable volume, these costs can spiral out of control. A self-hosted model has a higher initial setup cost (hardware and engineering) but transitions to a predictable, fixed operational expense, which is often far more economical at scale.

### Customization & Control
Self-hosting gives you complete control over the model. You can fine-tune it on your own proprietary datasets to improve performance on specific tasks, creating a competitive advantage. You also control model versions, update schedules, and uptime, ensuring the service aligns perfectly with your business needs.

## Getting Started
Follow these steps to set up and run the application locally.

### Prerequisites
VSCode or a similar code editor.

Git installed on your local machine.

Conda or Miniconda installed.

Python 3.9 or higher.

A unique API Key from NAI. This is assigned per user from the Model Endpoint

The Endpoint URL for the LLM you intend to use.

### 1. Clone the Repository
Clone this repository to your local machine using Git:

Bash

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
### 2. Create and Activate the Conda Environment
Create a dedicated Conda environment and install the required packages.

Bash

# Create the environment
conda create -n private_llm_ui python=3.10 -y

# Activate the environment
conda activate private_llm_ui

# Install dependencies
pip install streamlit requests pypdf
### 3. Configure Your Credentials
For security, we'll use Streamlit's built-in secrets management. Do not hard-code your API key in the app.py file.

Create a folder named .streamlit in the root of your project directory.

Inside that folder, create a file named secrets.toml.

Add your API key and model information to the secrets.toml file like this:

Ini, TOML

# .streamlit/secrets.toml

API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
MODEL_NAME = "iep-gpt-oss-120b"
API_URL = "https://ai.nutanix.com/api/v1/chat/completions"
### 4. Edit the Script
There are two parts of the app.py script that you will need to edit:

API Key: This is a unique key that identifies you to the LLM provider. You will need to replace the placeholder in the secrets.toml file with your own key.

Endpoint URL: This is the URL of the LLM you want to use. You will need to replace the placeholder in the secrets.toml file with the correct URL.

### 5. Run the Application
Launch the Streamlit application from your terminal:

Bash

streamlit run app.py
A new tab should open in your default web browser at http://localhost:8501.

## How to Use
Chat with the Model: Type a question or prompt into the input box at the bottom of the screen and press Enter.

Use a Document for Context: Click the "Browse files" button in the sidebar to upload a PDF document. The application will extract the text and provide it as context for your next prompt.

Conversation History: The application keeps track of your current conversation session

