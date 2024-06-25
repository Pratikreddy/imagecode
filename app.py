import streamlit as st
import base64
import mimetypes
import google.generativeai as genai
import os

# Configure the Gemini API key
api_key = "AIzaSyBrQemIQoAT6gZLI7pvuV-mmM6OZXATbE8"
genai.configure(api_key=api_key)

# Helper function to read image bytes and encode them in base64
def read_image_base64(image_path):
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Helper function to get MIME type based on file extension
def get_mime_type(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type or 'application/octet-stream'

# Function to process images and send to Gemini Vision API
def process_image_gemini(image_path, prompt, model_name='gemini-1.5-flash'):
    image_data = {
        'mime_type': get_mime_type(image_path),
        'data': read_image_base64(image_path)
    }

    # Prepare content
    content = [prompt, image_data]

    # Create model instance
    model = genai.GenerativeModel(model_name)

    # Generate content
    try:
        response = model.generate_content(
            content,
            generation_config={"response_mime_type": "application/json"}
        )
        return response
    except Exception as e:
        return f"An error occurred with image {os.path.basename(image_path)}: {e}"

# Function to send text prompt to Gemini API
def process_text_gemini(prompt, model_name='gemini-1.5-flash'):
    # Create model instance
    model = genai.GenerativeModel(model_name)

    # Generate content
    try:
        response = model.generate_content(
            [prompt],
            generation_config={"response_mime_type": "application/json"}
        )
        return response
    except Exception as e:
        return f"An error occurred: {e}"

# Initialize the system message
system_message = """
You are a virtual assistant providing HS Code information. Be professional and informative.
Do not make up any details you do not know always sound smart and refer to yourself as Jarvis.

We help you find the right HS Code for your products quickly and accurately. Save time and avoid customs issues with our automated HS Code lookup tool.
"""

# Initialize the products list (empty for now)
products = []

# Streamlit app setup
st.set_page_config(page_title="HS Code Lookup System", layout="wide")

st.title("HS Code Lookup System")
st.write("Automated and accurate HS Code information at your fingertips.")

# Initialize chat history as a session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "system", "content": system_message}]
if "input_buffer" not in st.session_state:
    st.session_state.input_buffer = ""

# Input for chat messages
user_input = st.text_input("Type your message here:", key="input_buffer")

# File upload for image
uploaded_file = st.file_uploader("Upload an image file", type=["jpg", "jpeg", "png"])

# Function to handle message sending and processing
def send_message():
    user_prompt = st.session_state.input_buffer
    imgpath = "temp_image.png"

    if not user_prompt and not uploaded_file:
        st.write("Please provide a text input, an image, or both.")
    else:
        if uploaded_file:
            # Save the uploaded file temporarily
            with open(imgpath, "wb") as f:
                f.write(uploaded_file.getbuffer())
            prompt = f"{system_message}\n{user_prompt}"
            response = process_image_gemini(imgpath, prompt)
        else:
            response = process_text_gemini(f"{system_message}\n{user_prompt}")

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

# Display product details (empty for now)
st.write("## Product Catalog")
st.write("### Select a product from below and refer to it in the chat (Reference Only):")
product_var = st.selectbox("Select Product (Reference Only):", ["No products available"])
