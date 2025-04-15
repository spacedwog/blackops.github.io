# -----------------------------
# ai/ocr_rfid.py
# -----------------------------
import os
import cv2
import base64
import pytesseract
from PIL import Image
import streamlit as st
from io import BytesIO
from core.github_utils import get_repo_info

def stream_camera():
    cap = cv2.VideoCapture(0)

    # Estilo inspirado na Twitch
    st.markdown("""...""", unsafe_allow_html=True)  # O mesmo CSS que você já colocou

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

        # --- GitHub integration ---
        token = os.getenv("GITHUB_TOKEN")  # Segura via variável de ambiente
        repo_name = "openai/whisper"
        repo_info = get_repo_info(repo_name, token)

        # Chat HTML com mensagens fixas
        st.markdown("""<div class="chat-box">""", unsafe_allow_html=True)
        
        # Mensagens GitHub como bot
        if "error" in repo_info:
            st.markdown(f"""<div class="chat-message"><span class="chat-username">[github_bot]:</span> Erro: {repo_info['error']}</div>""", unsafe_allow_html=True)
        else:
            github_chat = [
                f"🔗 Repositório: `{repo_info['name']}`",
                f"📝 Descrição: {repo_info['description']}`",
                f"📦 Linguagem: `{repo_info['language']}`",
                f"⭐ Estrelas: `{repo_info['stars']}`",
                f"🐞 Issues Abertas: `{repo_info['open_issues']}`",
                f"🕒 Último Commit: `{repo_info['last_commit']}`"
            ]
            for line in github_chat:
                st.markdown(f"""<div class="chat-message"><span class="chat-username">[github_bot]:</span> {line}</div>""", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

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
            <div style="display: flex; justify-content: center; align-items: center;">
                <img src="data:image/jpeg;base64,{image_to_base64(frame_rgb)}" class="stream-frame"/>
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