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

system_message = """
You are a virtual assistant providing HS Code information. Be professional and informative.
do not make up any details you do not know always sound smart and refer to youreself as jarvis.

only list the prodcuts when asked be less chatty and more inquisitive

We help you find the right HS Code for your products quickly and accurately. Save time and avoid customs issues with our automated HS Code lookup tool.

Product List:

"""

# Initialize the products list (empty for now)
products = [
    {"hs_code": "84137099", "name": "CENTRIFUGAL FIRE PUMP HORIZONTAL SPLIT CASE", "definisi": "Pompa pemadam kebakaran yang menggunakan prinsip sentrifugal untuk memompa air, dan memiliki desain casing yang dapat dibuka secara horizontal", "bahan": "Besi Baja / Logam"},
    {"hs_code": "40101900", "name": "CONVEYOR BELT, FABRIC BELT; 2400 MM X EP 200 X 4 PLY X 10 MM X 4 MM; GRADE M", "definisi": "Sabuk konveyor kain dengan spesifikasi sebagai berikut: Lebar: 2400 milimeter (2,4 meter), Ketebalan: 10 milimeter, Ketebalan lapisan kain: 4 milimeter, Jumlah lapisan kain: 4, Kekuatan tarik: EP 200, Kelas: M", "bahan": "Serat Polyester (EP)"},
    {"hs_code": "73181510", "name": "M12 x 120mm Lg Hex Hd HT Bolt BZP", "definisi": "Baut kepala heksagonal besar dengan kekuatan tarik tinggi dan lapisan seng cerah, yang biasa digunakan dalam berbagai aplikasi industri dan konstruksi. M12: Ini mengacu pada diameter ulir metrik baut, yang dalam hal ini adalah 12 milimeter, 120mm: Ini menunjukkan panjang baut, yaitu 120 milimeter, Lg Hex Hd: Ini adalah singkatan dari Large Hex Head", "bahan": "Bright Zinc Plated"},
    {"hs_code": "73181590", "name": "Bolt (M27X260X30)", "definisi": "Baut heksagonal berkekuatan tinggi dengan diameter ulir metrik 27 milimeter, panjang 260 milimeter, dan tinggi kepala 30 milimeter. Baut ini umumnya digunakan dalam aplikasi industri di mana kekuatan dan keandalan tinggi", "bahan": "Bright Zinc Plated"},
    {"hs_code": "73182100", "name": "MAKE: SEW - RETAINING RING DIN472 100X3-FS", "definisi": "Cincin penahan adalah komponen mekanis yang digunakan untuk menahan komponen lain di tempatnya. Cincin penahan ini memiliki diameter luar 100 mm dan ketebalan 3 mm", "bahan": "Stainless Steel"},
    {"hs_code": "73182100", "name": "CRUSHER SP; OIL RETAINING RING; DW NO:27-02 0861/B; PN:07; TYPE: ESC-584; EQU: COAL CRUSHER SCOOP COUPLING; OEM: ELECON", "definisi": "Cincin penahan oli yang digunakan pada sekop penyapu crusher batu bara. Cincin penahan ini berfungsi untuk menahan oli agar tidak bocor dari sekop penyapu. Cincin penahan ini memiliki diameter luar 100 mm dan ketebalan 3 mm", "bahan": "Stainless Steel"},
    {"hs_code": "73194020", "name": "CLAMP, C: 4IN FORGED ULTRA STRONG DROP STEEL CLAMP BAR TYPE; DAWN; JAW OPENING 100MM; THROAT DEPTH 60MM", "definisi": "Klem batang baja cor tipe C yang kuat. Klem ini memiliki panjang 4 inci dan memiliki rahang yang dapat dibuka hingga 100 mm. Klem ini terbuat dari baja cor dan memiliki lapisan krom untuk melindunginya dari karat.", "bahan": "Stainless Steel"},
    {"hs_code": "40101200", "name": "CONVEYOR BELT TYPE: 2200 EP 630/4 6+3 Y ME BELT CONVEYOR BELT CONVEYOR EP630/4 2200MM, 6+3MM COVER, DIN Y GRADE; 151MT/ROLL 711016770 231561", "definisi": "Sabuk konveyor tipe EP630/4 dengan lebar 2200 mm, ketebalan cover 6+3 mm, dan grade DIN Y. Sabuk konveyor ini terbuat dari bahan polyester dan memiliki lapisan karet. Sabuk konveyor ini dapat menahan beban hingga 630 kg/m.", "bahan": "Polyester"},
    {"hs_code": "73079910", "name": "LUBRICATION FITTING ASSORTMENT: AUTOMOTIVE HYDRAULIC GREASE NIPPLE; 12 SIZES: SAE, ANF, BSP, METRIC, BSF", "definisi": "Set alat yang digunakan untuk melumasi komponen-komponen otomotif. Set alat ini terdiri dari 12 ukuran nipple pelumas yang berbeda, termasuk ukuran SAE, ANF, BSP, metrik, dan BSF.", "bahan": "-"},
    {"hs_code": "40101200", "name": "STUD, RECESSED: THREADED BOTH END; 900MM LENGTH; C/W 4 EACH M42 NUTS; USED ON ELECTROMAGNETIC VIBRATORY MODEL FV890 EQ 2482", "definisi": "Sebuah baut panjang berulir khusus yang digunakan pada alat getar elektromagnetik model FV890 dengan kode komponen EQ 2482.", "bahan": "Polyester"},
    {"hs_code": "84749000", "name": "A061-97 SAFETY DOOR MATEST", "definisi": "Unknown", "bahan": "Unknown"},
    {"hs_code": "84749000", "name": "CRUSHER SP; SHAFT SLEEVE; DW NO: 27-02-0861/B; PN: 16; TYPE: ESC-584; EQU: COAL CRUSHER SCOOP COUPLING; OEM: ELECON", "definisi": "Unknown", "bahan": "Unknown"},
    {"hs_code": "84818099", "name": "2\" BSP LEVER OPERATED BALL VALVE", "definisi": "Unknown", "bahan": "Unknown"},
    {"hs_code": "84818099", "name": "3 WAY BALL VALVE CW ACTUATOR", "definisi": "Unknown", "bahan": "Unknown"},
    {"hs_code": "84818099", "name": "3/4\" NON RETURN VALVE", "definisi": "Unknown", "bahan": "Unknown"},
    {"hs_code": "84818099", "name": "BOW: BOW SWING SHAVE USED ON 250 HDDS", "definisi": "Unknown", "bahan": "Unknown"},
    {"hs_code": "84833090", "name": "BSH, TPR, M, 4188 BORE, IRON", "definisi": "Unknown", "bahan": "Unknown"},
    {"hs_code": "84833090", "name": "BUSH; PN: POS 112; EQU: CONTROL VALVE SPINDLE PACKING ASSLY; OEM; BHEL; ODEL; ENK 40/56-3", "definisi": "Unknown", "bahan": "Unknown"},
    {"hs_code": "84314940", "name": "CA31407; HOT CUPPED END BIT; LH; 225; 1425; 2850;; MT; HC", "definisi": "Unknown", "bahan": "Unknown"},
    {"hs_code": "84314990", "name": "6806-S95; S-POSILOK WELDON ADAPTER; ESCO GRN", "definisi": "Unknown", "bahan": "Unknown"},
    {"hs_code": "84811019", "name": "CONTROL VALVE & SOLENOID ASSY USED ON TRANSMISSION MG5091SC; 200C; 200/225, MD300", "definisi": "Unknown", "bahan": "Unknown"}
]


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

# Display product details
st.write("## Product Catalog")
st.write("### Select a product from below and refer to it in the chat (Reference Only):")
product_var = st.selectbox("Select Product (Reference Only):", ["No products available"])
