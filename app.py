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
do not make up any details you do not know always sound smart and refer to youresefl as jarvis.

We help you find the right HS Code for your products quickly and accurately. Save time and avoid customs issues with our automated HS Code lookup tool.

Product List:
CENTRIFUGAL FIRE PUMP HORIZONTAL SPLIT CASE
* HS Code: 84137099

CONVEYOR BELT, FABRIC BELT; 2400 MM X EP 200 X 4 PLY X 10 MM X 4 MM; GRADE M
    * HS Code: 40101900

M12 x 120mm Lg Hex Hd HT Bolt BZP
* HS Code: 73181510

Bolt (M27X260X30)
* HS Code: 73181590

MAKE: SEW - RETAINING RING DIN472 100X3-FS
* HS Code: 73182100

CRUSHER SP; OIL RETAINING RING; DW NO:27-02 0861/B; PN:07; TYPE: ESC-584; EQU: COAL CRUSHER SCOOP COUPLING; OEM: ELECON
* HS Code: 73182100

CLAMP, C: 4IN FORGED ULTRA STRONG DROP STEEL CLAMP BAR TYPE; DAWN; JAW OPENING 100MM; THROAT DEPTH 60MM
* HS Code: 73194020

CONVEYOR BELT TYPE: 2200 EP 630/4 6+3 Y ME BELT CONVEYOR BELT CONVEYOR EP630/4 2200MM, 6+3MM COVER, DIN Y GRADE; 151MT/ROLL 711016770 231561
* HS Code: 40101200

LUBRICATION FITTING ASSORTMENT: AUTOMOTIVE HYDRAULIC GREASE NIPPLE; 12 SIZES: SAE, ANF, BSP, METRIC, BSF
* HS Code: 73079910

STUD, RECESSED: THREADED BOTH END; 900MM LENGTH; C/W 4 EACH M42 NUTS; USED ON ELECTROMAGNETIC VIBRATORY MODEL FV890 EQ 2482
* HS Code: 40101200

HS CODE - 84749000
1. A061-97 SAFETY DOOR MATEST
2. CRUSHER SP; SHAFT SLEEVE; DW NO: 27-02-0861/B; PN: 16; TYPE: ESC-584; EQU: COAL CRUSHER SCOOP COUPLING; OEM: ELECON
3. DAMPER: VIBRATION DAMPENER M140 MATERIAL DURO 40DR CRUSHER 23050 WD2
4. HAMMER: HAMMER ROTOR FOR HAMMER MILL CRUSHER SAMPLER
5. HTD SPROCKET P80-14M-170J
6. LABYRINTH SEAL RING: SEALING; 112MM ID X 128 MM OD; LABYRINTH; BEARING ASSEMBLY
7. MAIN DR SFT-FLG MTD MACHINING
8. MAKE: SEW - CABLE GLAND
9. ROD EYE: CONNECTOR, ROD END; ROD EYE; USED ON GUNDLACH 6024 DSA CRUSHER COAL PREPARATION PLANT
10. SCREEN, CRUSHER SC6T: FOR SC6T HAMMERMILL CRUSHER ARRANGEMENT DWG NO 23050 WD2; SAMPLING SYSTEM; COAL CHAIN UPGRADE

HS CODE - 84818099
1. 2" BSP LEVER OPERATED BALL VALVE
2. 3 WAY BALL VALVE CW ACTUATOR
3. 3/4" NON RETURN VALVE
4. BOW: BOW SWING SHAVE USED ON 250 HDDS
5. CHECK VALVE (4BAR)
6. CONTROL VALVE & SOLENOID ASSY USED ON TRANSMISSION MG5091SC; 200C; 200/225, MD300
7. DEMCO BUTTERFLY VALVE
8. DISC VALVE KIT FOR CORING PUMP (AR VERSION)
9. DN50 HP Y-PATTERN GLOBE VALVE: DN50 HP Y-PATTERN GLOBE VALVE 01Y#1500 BODY MATERIAL: A105 STEM, DISC, SEAT: 17CR, STELLITE, STELLITE CONNECTION: BUTT WELD END FACE TO FACE: 279MM ACTUATION: HANDWHEEL-ACTUATOR
10. OVERCENTRE VALVE CARTRIDGE

HS CODE - 84314940
1. CA31407; HOT CUPPED END BIT; LH; 225; 1425; 2850;; MT; HC
2. CUTTING EDGE (25MM)
3. EDGE CUTTING MIDDLE
4. END BIT R/H (55MM)
5. HOT CUPPED END BIT; RH; 225; 1425; 2850;; MT; HC
6. LA6227HHD; RIBBED CUT EDGE; ESCO GRN
7. N5LWS-2; NEMISYS LOWER WING SHROUD; ESCO GRN
8. RIBBED CUT EDGE; ESCO GRN
9. TAW120X760-1; TOPLOK WING SHROUD; ESCO GRN
10. TBC140X490-1B; TOPLOK LIP SHROUD; ESCO GRN

HS CODE - 84833090
1. BSH, TPR, M, 4188 BORE, IRON
2. BUSH; PN: POS 112; EQU: CONTROL VALVE SPINDLE PACKING ASSLY; OEM; BHEL; ODEL; ENK 40/56-3
3. BUSHING (BI-METAL)
4. BUSHING (BRONZE)
5. BUSHING, TAPERED LOCKING ASSY TO LOCK CONVEYOR PULLEY TO SHAFT; COAL HANDLING CONVEYORS-CPP
6. BUSHING, TAPERED; LOCKING ASSEMBLY TO LOCK CONVEYOR PULLEY TO SHAFT; COAL HANDLING CONVEYORS-CPP
7. DRY BUSH | WASHER
8. GE BEARING
9. MAST PULLEY BUSH
10. SPHERICAL PLAIN BRG

HS CODE - 84314990
1. 6806-S95; S-POSILOK WELDON ADAPTER; ESCO GRN
2. 85SV2VX; SV2 POINT; ESCO GRN
3. BOTTOM ROLLER S/F (D7G)
4. CARRIER ROLLER ASSLY
5. CORNER WEAR SHOE; ESCO GRN
6. DRP RIPPER POINT; ESCO GRN
7. EVERSHARP ECC SHROUD BASE; CLR COAT
8. FRONT IDLER ASSLY
9. HOT CUPPED END BIT; LH; 225; 1425; 2850;; MT; HC
10. MASTER SHOE 24" (D7G)

HS CODE - 84811019
1. CONTROL VALVE & SOLENOID ASSY USED ON TRANSMISSION MG5091SC; 200C; 200/225, MD300
2. FLOW CONTROL VALVE
3. MINIMUM PRESSURE VALVE USED FOR XHP900/350 COMPRESSOR
4. NEEDLE VALVE
5. PRESSURE REDUCING VALVE
6. PRESSURE REDUCING VALVE 1/2" BSP
7. SPARES FOR WATER QUALITY MONITORING SYSTEM, SAMPLE PRESSURE RELIEF VALVE - SRV, SPRING LOADED, 8NB (1/4"), SCREWED NPT(M), 8NB (1/4"), OD DOUBLE FERRULE, LIQUID, 33 KG/CM2, 0 TO 6 KG/CM2, BODY-SS316, TRIM-SS316, MTC
8. SWAGELOK V-SERIES MANIFOLD
9. VALVE, AIR PRESSURE RELIEF; QUICK RELEASE; AIR BRAKE SYSTEM; PART NO: KN32011
10. VALVE, AIR PRESSURE RELIEF; QUICK RELEASE; AIR BRAKE SYSTEM

Contact Information:
- Email: support@hscodefinder.com
- Phone: +1 234 567 8901
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

        # Extracting relevant content from the response
        try:
            if isinstance(response, str):
                st.session_state.chat_history.append({"role": "assistant", "content": response})
            else:
                message_content = response.candidates[0].content.parts[0].text
                st.session_state.chat_history.append({"role": "assistant", "content": message_content})
        except Exception as e:
            st.session_state.chat_history.append({"role": "assistant", "content": f"An error occurred: {e}"})

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
