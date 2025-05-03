# -----------------------------
# ./app.py
# -----------------------------
import time
import serial
import platform
import streamlit as st
from database.db import UsuarioDB
from auth.oauth import OAuthGitHub
from auth.blackboard import BlackboardValidator
from dashboard.github_dashboard import GitHubDashboard

# OCR e imagem
import os
import pytesseract
from datetime import date

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Verifica o sistema operacional e ajusta o caminho do Tesseract
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
elif platform.system() == "Linux":
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"  # geralmente o local padrão

if platform.system() == "Windows":
    path_win = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if os.path.exists(path_win):
        pytesseract.pytesseract.tesseract_cmd = path_win
elif platform.system() == "Linux":
    path_linux = "/usr/bin/tesseract"
    if os.path.exists(path_linux):
        pytesseract.pytesseract.tesseract_cmd = path_linux

class GitHubDashboardApp:

    def __init__(self):
        self.db = UsuarioDB()
        self.auth = OAuthGitHub()
        self.blackboard = BlackboardValidator()
        self.user_data = None
    
    def run(self):
        # sourcery skip: extract-duplicate-method, extract-method
        st.set_page_config(page_title="BlackOps", page_icon="⚫")
        st.title("🔐 Login com GitHub")

        if "login_realizado" not in st.session_state:
            st.session_state.login_realizado = False

        if not st.session_state.login_realizado:
            login_input = st.text_input("Digite seu login do GitHub:", key="login_input")

            self.user_data = self.auth.callback()

            if self.user_data:
                if self.blackboard.validar_usuario(self.user_data, login_input):
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
                    "🛡️ Cibersegurança",
                    "🔄 Relay(Arduino)"
                ])

                with abas[0]:
                    self.dashboard.exibir_perfil()

                with abas[1]:
                    self.dashboard.exibir_repositorios()

                with abas[2]:
                    self.dashboard.exibir_data_science()

                with abas[3]:
                    self.auth.exibir_cyberseguranca()

                with abas[4]:
                    # Configurar a porta serial
                    try:
                        arduino = serial.Serial('COM3', 9600, timeout=1)  # Altere 'COM3' conforme seu sistema
                        time.sleep(2)  # Aguarda a conexão

                        st.title("Monitor de Relé - Arduino")

                        if arduino:
                            if st.button("Atualizar estado do relé"):
                                arduino.flushInput()
                                leitura = arduino.readline().decode().strip()
                                if leitura:
                                    estado = "Ligado" if leitura == "STATUS" else "Desligado"
                                    st.success(f"Estado do relé: {estado}")
                                else:
                                    st.warning("Nenhum dado recebido.")
                        else:
                            st.error("Não foi possível conectar ao Arduino.")
                    except serial.SerialException:
                        arduino = None

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