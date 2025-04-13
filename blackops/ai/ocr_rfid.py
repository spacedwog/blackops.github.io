# -----------------------------
# ai/ocr_rfid.py
# -----------------------------
import cv2
import streamlit as st

def stream_camera():
    cap = cv2.VideoCapture(0)

    # Estilo para centralizar o vídeo
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
    st.info("🎥 Transmitindo da câmera...")

    video_placeholder = st.empty()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.error("❌ Falha ao capturar imagem da câmera.")
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Exibe o frame dentro de uma div centralizada com classe customizada
        video_placeholder.markdown(
            f"""
            <div class="centered-video">
                <img src="data:image/jpeg;base64,{image_to_base64(frame)}" class="video-frame"/>
            </div>
            """, unsafe_allow_html=True
        )

        if stop:
            st.warning("🛑 Transmissão encerrada.")
            break

    cap.release()


def image_to_base64(image):
    import base64
    from io import BytesIO
    from PIL import Image
    buf = BytesIO()
    Image.fromarray(image).save(buf, format="JPEG")
    return base64.b64encode(buf.getvalue()).decode()