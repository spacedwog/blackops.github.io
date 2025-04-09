import pandas as pd
import streamlit as st
from database.db import UsuarioDB
from auth.oauth import OAuthGitHub
from auth.blackboard import BlackboardValidator
from dashboard.github_dashboard import GitHubDashboard

# OCR e imagem
import os
import cv2
import tempfile
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class GitHubDashboardApp:
    def __init__(self):
        self.db = UsuarioDB()
        self.auth = OAuthGitHub()
        self.validator = BlackboardValidator()
        self.user_data = None

    def ler_rfid_via_camera(self):
        st.info("📷 Posicione o cartão RFID com código visível.")
        if st.button("🔍 Escanear Cartão RFID"):
            cap = cv2.VideoCapture(0)
            st_frame = st.empty()

            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_image:
                for _ in range(30):
                    ret, frame = cap.read()
                    if ret:
                        st_frame.image(frame, channels="BGR", caption="Imagem capturada")
                cv2.imwrite(temp_image.name, frame)
                cap.release()

            # Agora fora do `with`, o arquivo está liberado para uso/remover
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
            config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEF'
            texto = pytesseract.image_to_string(thresh, config=config).strip().upper()

            if texto:
                st.success(f"✅ UID detectado: `{texto}`")
                uid_detectado = texto
                if not self.db.get_usuario_por_uid(uid_detectado):
                    st.info("🔒 Cartão não registrado. Registrando novo usuário.")
                    nome = self.user_data.get("name")
                    login_github = self.user_data.get("login")
                    nivel = "Usuario"
                    self.db.registrar_cartao(uid_detectado, nome, login_github, nivel)
                    st.success("✅ Cartão registrado com sucesso!")
                else:
                    usuario = self.db.get_usuario_por_uid(uid_detectado)
                    df = pd.DataFrame([{
                        "Nome": usuario[1],
                        "Login": usuario[2],
                        "Nível": usuario[3],
                        "Último Acesso": usuario[4]
                    }])
                    st.table(df)
                    st.success(f"✅ Bem-vindo, {usuario[1]}!")
            else:
                st.error("❌ Não foi possível reconhecer o texto.")

            # Agora podemos remover com segurança
            os.remove(temp_image.name)


    def run(self):
        st.set_page_config(page_title="GitHub OAuth Dashboard", page_icon="🐙")
        st.title("🔐 Login com GitHub")

        if "login_realizado" not in st.session_state:
            st.session_state.login_realizado = False

        if not st.session_state.login_realizado:
            login_input = st.text_input("Digite seu login do GitHub:", key="login_input")

            self.user_data = self.auth.callback()

            if self.user_data:
                if self.validator.validar_usuario(self.user_data, login_input):
                    self.db.salvar_usuario(self.user_data)
                    st.session_state.login_realizado = True
                    st.rerun()
                else:
                    st.error("❌ Acesso negado: usuário inválido.")
            else:
                self.auth.login_button()

        else:
            if not self.user_data:
                self.user_data = self.auth.get_user_from_token()

            if self.user_data:
                self.dashboard = GitHubDashboard(self.user_data)

                abas = st.tabs([
                    "👤 Perfil",
                    "📦 Repositórios",
                    "📈 Data Science",
                    "🧱 Firewall e Relay",
                    "🛡️ Cibersegurança",
                    "📷 Leitor RFID OCR"
                ])

                with abas[0]:
                    self.dashboard.exibir_perfil()

                with abas[1]:
                    self.dashboard.exibir_repositorios()

                with abas[2]:
                    self.dashboard.exibir_data_science()

                with abas[3]:
                    self.dashboard.exibir_relay_firewall()

                with abas[4]:
                    self.auth.exibir_cyberseguranca()

                with abas[5]:
                    self.ler_rfid_via_camera()

                if st.button("🚪 Logout"):
                    st.session_state.login_realizado = False
                    st.session_state.access_token = None
                    st.rerun()

            else:
                st.warning("⚠️ Sessão expirada. Faça login novamente.")
                st.session_state.login_realizado = False
                st.session_state.access_token = None
                st.rerun()

# Executa a aplicação
if __name__ == "__main__":
    app = GitHubDashboardApp()
    app.run()