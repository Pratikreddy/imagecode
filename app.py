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
        return response.text
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
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

# Initialize the system message
system_message = """
"""

# Initialize the products list (empty for now)
products = []

# Streamlit app setup
st.set_page_config(page_title="HS Code Lookup System", layout="wide")

st.title("HS Code Lookup System")
st.write("Automated and accurate HS Code information at your fingertips.")

# Input for chat messages
user_prompt = st.text_input("Type your message here:")

# File upload for image
uploaded_file = st.file_uploader("Upload an image file", type=["jpg", "jpeg", "png"])

# Send button
if st.button("Send"):
    if not user_prompt and not uploaded_file:
        st.write("Please provide a text input, an image, or both.")
    else:
        if uploaded_file and user_prompt:
            # Save the uploaded file temporarily
            with open("temp_image.png", "wb") as f:
                f.write(uploaded_file.getbuffer())
            prompt = f"{system_message}\n{user_prompt}"
            response = process_image_gemini("temp_image.png", prompt)
        elif uploaded_file:
            # Save the uploaded file temporarily
            with open("temp_image.png", "wb") as f:
                f.write(uploaded_file.getbuffer())
            response = process_image_gemini("temp_image.png", system_message)
        else:
            response = process_text_gemini(f"{system_message}\n{user_prompt}")

        if user_prompt:
            st.markdown(f"**You:** {user_prompt}")
        if uploaded_file:
            st.markdown(f"**You uploaded an image:** {uploaded_file.name}")

        st.markdown(f"**Jarvis:** {response}")

# Product catalog display (for reference only, empty for now)
st.write("## Product Catalog")
st.write("### Select a product from below and refer to it in the chat (Reference Only):")
product_var = st.selectbox("Select Product (Reference Only):", ["No products available"])
