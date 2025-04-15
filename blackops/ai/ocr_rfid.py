# -----------------------------
# ai/ocr_rfid.py
# -----------------------------
import cv2
import streamlit as st
import pytesseract
from PIL import Image
import base64
from io import BytesIO

def stream_camera():
    cap = cv2.VideoCapture(0)

    st.markdown("""
        <style>
        .centered-video {
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .video-frame {
            width: 100%;
            max-width: 800px;
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(0,0,0,0.2);
        }
        </style>
    """, unsafe_allow_html=True)

    stop = st.button("⏹️ Parar transmissão", key="stop_stream")
    capture = st.button("📸 Capturar e processar OCR", key="capture_ocr")

    st.info("🎥 Transmitindo da câmera...")
    video_placeholder = st.empty()
    ocr_result_placeholder = st.empty()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.error("❌ Falha ao capturar imagem da câmera.")
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Exibe vídeo ao vivo
        video_placeholder.markdown(
            f"""
            <div class="centered-video">
                <img src="data:image/jpeg;base64,{image_to_base64(frame_rgb)}" class="video-frame"/>
            </div>
            """,
            unsafe_allow_html=True
        )

        if capture:
            processed = preprocess_image_for_ocr(frame_rgb)
            text = pytesseract.image_to_string(processed, lang="eng")  # ou "por" para português

            # Exibe imagem binarizada e OCR
            ocr_result_placeholder.subheader("📖 Resultado do OCR:")
            ocr_result_placeholder.text(text)

            st.image(processed, caption="Imagem pré-processada (binarização adaptativa)", use_column_width=True)

        if stop:
            st.warning("🛑 Transmissão encerrada.")
            break

    cap.release()

def preprocess_image_for_ocr(image):
    """Melhora imagem para OCR em baixa luz."""
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    equalized = cv2.equalizeHist(gray)

    thresh = cv2.adaptiveThreshold(
        equalized, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )
    return thresh

def image_to_base64(image):
    buf = BytesIO()
    Image.fromarray(image).save(buf, format="JPEG")
    return base64.b64encode(buf.getvalue()).decode()