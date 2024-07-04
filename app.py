import streamlit as st
import base64
import mimetypes
import openai
import os
import requests
import json

# Load the OpenAI API key from Streamlit secrets
api_key = st.secrets["openai"]["api_key"]
openai.api_key = api_key

# System prompt for the AI model
system_message = ""

# Helper function to read image bytes and encode them in base64
def read_image_base64(image_path):
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Function to send a prompt (text and/or image) to OpenAI API
def process_prompt_openai(system_prompt, user_prompt, image_path=None):
    base64_image = read_image_base64(image_path) if image_path else None

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": "gpt-4o",
        "response_format": {"type": "json_object"},
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"system prompt : {system_prompt}, user_prompt : {user_prompt}, expected format : JSON."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ] if base64_image else [
                    {
                        "type": "text",
                        "text": f"system prompt : {system_prompt}, user_prompt : {user_prompt}, expected format : JSON."
                    }
                ]
            }
        ],
        "max_tokens": 3000
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()

# Streamlit app setup
st.set_page_config(page_title="HS Code Lookup System", layout="wide")

st.title("HS Code Lookup System")
st.write("Automated and accurate HS Code information at your fingertips.")

# Initialize chat history as a session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "input_buffer" not in st.session_state:
    st.session_state.input_buffer = ""

# Input for chat messages
user_input = st.text_input("Type your message here:", key="input_buffer")

# File upload for image
uploaded_file = st.file_uploader("Upload an image file", type=["jpg", "jpeg", "png"])

# Function to handle message sending and processing
def send_message():
    user_prompt = st.session_state.input_buffer
    imgpath = "temp_image.png" if uploaded_file else None

    # Combine system message and chat history
    system_prompt = system_message + " ".join([msg["content"] for msg in st.session_state.chat_history])

    if not user_prompt and not uploaded_file:
        st.write("Please provide a text input, an image, or both.")
    else:
        if uploaded_file:
            # Save the uploaded file temporarily
            with open(imgpath, "wb") as f:
                f.write(uploaded_file.getbuffer())
        
        response = process_prompt_openai(system_prompt, user_prompt, imgpath)

        # Update chat history
        if user_prompt:
            st.session_state.chat_history.append({"role": "user", "content": user_prompt})
        if uploaded_file:
            st.session_state.chat_history.append({"role": "user", "content": f"Image: {uploaded_file.name}"})

        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.session_state.input_buffer = ""

    st.experimental_rerun()  # Trigger rerun to clear input and update chat history

# Display chat history
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(f"<div style='border: 2px solid blue; padding: 10px; margin: 10px 0; border-radius: 8px; width: 80%; float: right; clear: both;'>{message['content']}</div>", unsafe_allow_html=True)
    elif message["role"] == "assistant":
        st.markdown(f"<div style='border: 2px solid green; padding: 10px; margin: 10px 0; border-radius: 8px; width: 80%; float: left; clear: both;'>{message['content']}</div>", unsafe_allow_html=True)

# Send button
st.button("Send", on_click=send_message)
