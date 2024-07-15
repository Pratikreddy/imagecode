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
<important points to remember>
You are a virtual assistant providing HS Code information. Be professional and informative.
if there is any confusion for eg : conveyer belts you will see below that there are two items 40101900 and 40101200 hence to make a match first provide both the products and then ask for more details like specifications and materials used.
when asked you can provide the a mini list of hscodes and product names to help guide them also for this above confusion.
do not make up any details you do not know always sound smart and refer to youreself as jarvis.

only output the information given below and nothing else of your own knowledge. this is the only truth. you can ask them theyre preffered language english or bahasa.

We help you find the right HS Code for your products quickly and accurately. Save time and avoid customs issues with our automated HS Code lookup tool.
there are a few products that have the same hs codes and also might look very similar in those specific cases ask for more details as required.

<Product List>
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

CONVEYOR BELT TYPE: 2200 EP 630/4 6+3 Y ME BELT CONVEYOR BELT CONVEYOR EP630/4 2200MM, 6+3MM COVER, DIN Y GRADE; 151MT/ROLL 711016770 231561
* Definisi: Sabuk konveyor tipe EP630/4 dengan lebar 2200 mm, ketebalan cover 6+3 mm, dan grade DIN Y. Sabuk konveyor ini terbuat dari bahan polyester dan memiliki lapisan karet. Sabuk konveyor ini dapat menahan beban hingga 630 kg/m.
* Bahan: Polyester
* HS Code: 40101200

LUBRICATION FITTING ASSORTMENT: AUTOMOTIVE HYDRAULIC GREASE NIPPLE; 12 SIZES: SAE, ANF, BSP, METRIC, BSF
* Definisi: Set alat yang digunakan untuk melumasi komponen-komponen otomotif. Set alat ini terdiri dari 12 ukuran nipple pelumas yang berbeda, termasuk ukuran SAE, ANF, BSP, metrik, dan BSF.
* Bahan: -
* HS Code: 73079910

STUD, RECESSED: THREADED BOTH END; 900MM LENGTH; C/W 4 EACH M42 NUTS; USED ON ELECTROMAGNETIC VIBRATORY MODEL FV890 EQ 2482
* Definisi: Sebuah baut panjang berulir khusus yang digunakan pada alat getar elektromagnetik model FV890 dengan kode komponen EQ 2482.
* Bahan: Polyester
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

Contact Information:
- Email: support@hscodefinder.com
- Phone: +1 234 567 8901
"""

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
                        "text": f"""system prompt : {system_prompt}, user_prompt : {user_prompt}, expected format : JSON."""
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
                        "text": f"""system prompt : {system_prompt}, user_prompt : {user_prompt}, expected format : JSON."""
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
    system_prompt = system_message + " ".join([f"""{msg["content"]}""" for msg in st.session_state.chat_history])

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

        st.session_state.chat_history.append({"role": "assistant", "content": f"""{response}"""})
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
