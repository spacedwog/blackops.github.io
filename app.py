import logging
import pandas as pd
import streamlit as st
from database.db import UsuarioDB
from auth.oauth import OAuthGitHub
from auth.blackboard import BlackboardValidator
from dashboard.github_dashboard import GitHubDashboard

# OCR e imagem
import os
import cv2
import uuid
import tempfile
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class GitHubDashboardApp:
    def __init__(self):
        self.db = UsuarioDB()
        self.auth = OAuthGitHub()
        self.validator = BlackboardValidator()
        self.user_data = None
        
    def ler_rfid_via_camera(self, tentativas_max=3):
        st.info("📷 Posicione o cartão RFID com o código visível.")
        if st.button("🔍 Escanear Cartão RFID"):

            # Gera um nome de arquivo temporário fixo para sobrescrita
            temp_image_path = os.path.join(tempfile.gettempdir(), f"rfid_temp_{uuid.uuid4().hex}.png")

            sucesso = False
            uid_detectado = None

            for tentativa in range(1, tentativas_max + 1):
                st.write(f"🔄 Tentativa {tentativa} de {tentativas_max}...")

                cap = cv2.VideoCapture(0)
                st_frame = st.empty()

                for _ in range(30):
                    ret, frame = cap.read()
                    if ret:
                        st_frame.image(frame, channels="BGR", caption=f"Tentativa {tentativa}")
                cap.release()

                # Salva a imagem capturada (sobrescrevendo o mesmo arquivo)
                cv2.imwrite(temp_image_path, frame)

                # Processa OCR
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
                config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEF'
                texto = pytesseract.image_to_string(thresh, config=config).strip().upper()

                if texto:
                    uid_detectado = texto
                    st.success(f"✅ UID detectado: `{uid_detectado}`")
                    sucesso = True
                    break
                else:
                    st.warning("⚠️ Não foi possível reconhecer o texto nesta tentativa.")

            # Remove o arquivo temporário ao final
            if os.path.exists(temp_image_path):
                os.remove(temp_image_path)

            if not sucesso:
                st.error("❌ Falha ao ler o cartão RFID após múltiplas tentativas.")
                return

            # Processa o UID detectado
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
                if usuario[2] == self.user_data.get("login"):
                    st.success(f"✅ Bem-vindo, {usuario[1]}!")
                else:
                    st.error("❌ Acesso negado: usuário inválido.")


    def run(self):
        st.set_page_config(page_title="GitHub OAuth Dashboard", page_icon="🐙")
        st.title("🔐 Login com GitHub")

        if "login_realizado" not in st.session_state:
            st.session_state.login_realizado = False

        if not st.session_state.login_realizado:
            login_input = st.text_input("Digite seu login do GitHub:", key="login_input")

            #self.user_data = self.auth.callback()

            st.info(f"Login input: {login_input}")

            if self.user_data:
                st.info(f"User data: {self.user_data}")
                st.info(f"Login input: {login_input}")
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