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
system_message = """
You are a virtual assistant providing HS Code information. Be professional and informative.
Do not make up any details you do not know always sound smart and refer to yourself as Jarvis.

We help you find the right HS Code for your products quickly and accurately. Save time and avoid customs issues with our automated HS Code lookup tool.

Product List:
CENTRIFUGAL FIRE PUMP HORIZONTAL SPLIT CASE
* Definisi: Pompa pemadam kebakaran yang menggunakan prinsip sentrifugal untuk memompa air, dan memiliki desain casing yang dapat dibuka secara horizontal
* Bahan: Besi Baja / Logam
* HS Code: 84137099

CONVEYOR BELT, FABRIC BELT; 2400 MM X EP 200 X 4 PLY X 10 MM X 4 MM; GRADE M
* Definisi: sabuk konveyor kain dengan spesifikasi sebagai berikut:
    * Lebar: 2400 milimeter (2,4 meter)
    * Ketebalan: 10 milimeter
    * Ketebalan lapisan kain: 4 milimeter
    * Jumlah lapisan kain: 4
    * Kekuatan tarik: EP 200
    * Kelas: M
    * Bahan: Serat Polyester (EP)
    * HS Code: 40101900

M12 x 120mm Lg Hex Hd HT Bolt BZP
* Definisi: Baut kepala heksagonal besar dengan kekuatan tarik tinggi dan lapisan seng cerah, yang biasa digunakan dalam berbagai aplikasi industri dan konstruksi
    * M12: Ini mengacu pada diameter ulir metrik baut, yang dalam hal ini adalah 12 milimeter
    * 120mm: Ini menunjukkan panjang baut, yaitu 120 milimeter
    * Lg Hex Hd: Ini adalah singkatan dari "Large Hex Head," yang berarti baut memiliki kepala heksagonal besar untuk dikencangkan dengan kunci pas
* Bahan: Bright Zinc Plated
* HS Code: 73181510

Bolt (M27X260X30)
* Definisi: baut heksagonal berkekuatan tinggi dengan diameter ulir metrik 27 milimeter, panjang 260 milimeter, dan tinggi kepala 30 milimeter. Baut ini umumnya digunakan dalam aplikasi industri di mana kekuatan dan keandalan tinggi
    * M27: Ini mengacu pada diameter ulir metrik baut, yaitu 27 milimeter
    * 260: Ini menunjukkan panjang baut, yaitu 260 milimeter
    * 30: Ini menentukan tinggi kepala baut, yaitu 30 milimeter
* Bahan: Bright Zinc Plated
* HS Code: 73181590

MAKE: SEW - RETAINING RING DIN472 100X3-FS
* Definisi: Cincin penahan adalah komponen mekanis yang digunakan untuk menahan komponen lain di tempatnya. Cincin penahan ini memiliki diameter luar 100 mm dan ketebalan 3 mm
* Bahan: Stainless Steel
* HS Code: 73182100

CRUSHER SP; OIL RETAINING RING; DW NO:27-02 0861/B; PN:07; TYPE: ESC-584; EQU: COAL CRUSHER SCOOP COUPLING; OEM: ELECON
* Definisi: Cincin penahan oli yang digunakan pada sekop penyapu crusher batu bara. Cincin penahan ini berfungsi untuk menahan oli agar tidak bocor dari sekop penyapu. Cincin penahan ini memiliki diameter luar 100 mm dan ketebalan 3 mm
* Bahan: Stainless Steel
* HS Code: 73182100

CLAMP, C: 4IN FORGED ULTRA STRONG DROP STEEL CLAMP BAR TYPE; DAWN; JAW OPENING 100MM; THROAT DEPTH 60MM
* Definisi: Klem batang baja cor tipe C yang kuat. Klem ini memiliki panjang 4 inci dan memiliki rahang yang dapat dibuka hingga 100 mm. Klem ini terbuat dari baja cor dan memiliki lapisan krom untuk melindunginya dari karat.
* Bahan: Stainless Steel
* HS Code: 73194020
"""

# Helper function to read image bytes and encode them in base64
def read_image_base64(image_path):
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Helper function to get MIME type based on file extension
def get_mime_type(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type or 'application/octet-stream'

# Function to send image to OpenAI Vision API
def process_image_openai(image_path, prompt):
    base64_image = read_image_base64(image_path)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": "gpt-4-turbo",
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"data:image/jpeg;base64,{base64_image}"}
        ],
        "max_tokens": 300,
        "n": 1,
        "stop": None,
        "temperature": 1.0
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()

# Function to send text prompt to OpenAI API
def process_text_openai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content']

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
            response = process_image_openai(imgpath, prompt)
        else:
            response = process_text_openai(f"{system_message}\n{user_prompt}")

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
