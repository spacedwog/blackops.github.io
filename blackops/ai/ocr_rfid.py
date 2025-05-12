# -----------------------------
# ai/ocr_rfid.py
# -----------------------------
import cv2
import base64
import pytesseract
from PIL import Image
import streamlit as st
from io import BytesIO

def stream_camera():
    cap = cv2.VideoCapture(0)

    # Estilo inspirado na Twitch
    st.markdown("""
        <style>
        body {
            background-color: #0e0e10;
        }
        .twitch-header {
            font-size: 32px;
            font-weight: bold;
            color: #9146FF;
            text-align: left;
            padding: 10px 0;
        }
        .live-badge {
            background-color: red;
            color: white;
            border-radius: 5px;
            padding: 4px 10px;
            font-size: 14px;
            font-weight: bold;
            margin-left: 10px;
        }

        .glitch-wrapper {
            position: relative;
            display: inline-block;
        }

        .glitch-frame {
            border: 6px solid #9146FF;
            border-radius: 20px;
            box-shadow: 0 0 20px #9146FF, 0 0 30px #9146FF, 0 0 40px #9146FF;
            width: 100%;
            max-width: 720px;
            animation: neon-pulse 2s infinite alternate;
        }

        .glitch-frame::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border-radius: 20px;
            box-shadow: 0 0 10px #FF00FF, 0 0 20px #00FFFF;
            mix-blend-mode: screen;
            animation: glitch 1s infinite;
            pointer-events: none;
        }

        @keyframes neon-pulse {
            0% {
                box-shadow: 0 0 10px #9146FF, 0 0 20px #9146FF;
            }
            100% {
                box-shadow: 0 0 20px #9146FF, 0 0 40px #9146FF, 0 0 60px #9146FF;
            }
        }

        @keyframes glitch {
            0% {
                transform: translate(0px, 0px);
                opacity: 0.75;
            }
            20% {
                transform: translate(-2px, 1px);
            }
            40% {
                transform: translate(2px, -1px);
            }
            60% {
                transform: translate(-1px, 2px);
            }
            80% {
                transform: translate(1px, -2px);
            }
            100% {
                transform: translate(0px, 0px);
                opacity: 1;
            }
        }

        .chat-box {
            background-color: #18181B;
            border: 2px solid #2e2e31;
            border-radius: 10px;
            padding: 10px;
            color: white;
            height: 400px;
            overflow-y: auto;
            font-family: monospace;
            font-size: 14px;
        }

        .chat-message {
            margin-bottom: 5px;
        }
                
        .chat-indent {
            padding-left: 15px;
            opacity: 0.85;
        }

        .chat-username {
            color: #FF4ECC;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="twitch-header">🐺 Canal: Spacedwog <span class="live-badge">🔴 LIVE</span></div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2.5, 1])

    if 'capture' not in st.session_state:
        st.session_state.capture = False
    if 'stop' not in st.session_state:
        st.session_state.stop = False

    with col2:
        if st.button("📸 Capturar OCR"):
            st.session_state.capture = True
        if st.button("⏹️ Encerrar Live"):
            st.session_state.stop = True
            st.warning("🛑 Live encerrada.")
            cap.release()
            return

        st.markdown("### 💬 Chat da Live")

    with col1:
        st.info("🎥 Transmitindo ao vivo com overlay estilo Twitch!")
        video_placeholder = st.empty()
        ocr_result_placeholder = st.empty()
        processed_image_placeholder = st.empty()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.error("❌ Erro ao acessar a câmera.")
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        video_placeholder.markdown(
            f"""
            <div class="glitch-wrapper" style="display: flex; justify-content: center; align-items: center;">
                <img src="data:image/jpeg;base64,{image_to_base64(frame_rgb)}" class="glitch-frame"/>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.session_state.capture:
            with st.spinner("🧠 Processando OCR..."):
                processed = preprocess_image_for_ocr(frame_rgb)
                text = pytesseract.image_to_string(processed, lang="eng")

                ocr_result_placeholder.subheader("📖 Resultado do OCR")
                ocr_result_placeholder.code(text, language="text")

                processed_image_placeholder.image(
                    processed,
                    caption="📷 Imagem processada para OCR",
                    use_column_width=True
                )

            st.session_state.capture = False

        if st.session_state.stop:
            break

    cap.release()

def preprocess_image_for_ocr(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    equalized = cv2.equalizeHist(gray)
    thresh = cv2.adaptiveThreshold(
        equalized, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )
    return thresh

def image_to_base64(image):
    buf = BytesIO()
    Image.fromarray(image).save(buf, format="JPEG")
    return base64.b64encode(buf.getvalue()).decode()