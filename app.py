# -----------------------------
# ./app.py
# -----------------------------
import platform
import subprocess
import numpy as np
import pandas as pd
import streamlit as st
from database.db import UsuarioDB
from auth.oauth import OAuthGitHub
from auth.blackboard import BlackboardValidator
from dashboard.github_dashboard import GitHubDashboard

# OCR e imagem
import os
import cv2
import time
import pytesseract

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

    def ler_rfid_via_camera(self):  # sourcery skip: use-named-expression
        st.info("📷 Posicione o cartão RFID com código visível.")
        streaming_area = st.empty()

        if st.button("🔍 Iniciar Escaneamento ao Vivo"):
            uid = self.stream_camera_para_rfid(streaming_area, duracao=7)

            if uid:
                self.processar_uid_detectado(uid)
            else:
                st.error("❌ Não foi possível reconhecer o texto do cartão.")

    def stream_camera_para_rfid(self, st_frame, duracao=7):
        # sourcery skip: assign-if-exp, reintroduce-else, swap-if-else-branches
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        frame_final = None
        start_time = time.time()
        altura_linha = 0
        direcao = 1  # 1 para baixo, -1 para cima

        while time.time() - start_time < duracao:
            ret, frame = cap.read()
            if not ret:
                continue

            frame_final = frame.copy()  # Salva o último frame válido

            # Desenha a linha de scanner
            altura, largura, _ = frame.shape
            cv2.line(frame, (0, altura_linha), (largura, altura_linha), (0, 255, 0), 2)
            altura_linha += direcao * 15
            if altura_linha >= altura or altura_linha <= 0:
                direcao *= -1

            # Mostra vídeo no Streamlit
            st_frame.image(frame, channels="BGR", caption="📡 Escaneando...")

        cap.release()

        if frame_final is not None:
            return self.extrair_uid_da_imagem(frame_final)
        return None
    
    def extrair_uid_da_imagem(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Filtro de nitidez
        kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])
        sharpened = cv2.filter2D(gray, -1, kernel)

        # Contraste
        contrast = cv2.convertScaleAbs(sharpened, alpha=1.6, beta=0)
        _, thresh = cv2.threshold(contrast, 100, 255, cv2.THRESH_BINARY)

        config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEF'
        texto = pytesseract.image_to_string(thresh, config=config).strip().upper()
        return texto or None
    
    def processar_uid_detectado(self, uid_detectado):
        st.success("[OK] UID detectado: " + str(uid_detectado))
        usuario = self.db.get_usuario_por_uid(uid_detectado)
        if usuario:
            self.exibir_dados_usuario(usuario)

            if usuario[2] == self.user_data.get("login"):
                self.executar_acesso_autenticado(usuario, uid_detectado)
            else:
                st.error("❌ Acesso negado: usuário inválido.")

        else:
            self.extracted_from_processar_uid_detectado(uid_detectado)
    
    def extracted_from_processar_uid_detectado(self, uid_detectado):
        st.info("🔒 Cartão não registrado. Registrando novo usuário.")
        nome = self.user_data.get("name")
        login_github = self.user_data.get("login")
        self.db.registrar_cartao(uid_detectado, nome, login_github, "Usuario")
        st.success("✅ Cartão registrado com sucesso!")
        self.processar_uid_detectado(uid_detectado)

    def exibir_dados_usuario(self, usuario):
        df = pd.DataFrame([{
            "Nome": usuario[1],
            "Login": usuario[2],
            "Nível": usuario[3],
            "Último Acesso": usuario[4]
        }])
        st.table(df)

    def executar_acesso_autenticado(self, usuario, uid_detectado):
        self.mensagem = "[OK] Bem-vindo, " + usuario[3] + " " + usuario[2] + "! Seu ultimo acesso foi em " + usuario[4]
        st.success(self.mensagem)

        try:
            comando = "./executar_paineldns.ps1"
            resultado = subprocess.run(
                ["powershell", "-Command", comando],
                capture_output=True,
                text=True,
                shell=True
            )
            st.code(resultado.stdout or resultado.stderr)
        except Exception as e:
            st.error("Erro ao executar: " + str(e))

        self.db.atualizar_ultimo_acesso(uid_detectado)

    def run(self):
        st.set_page_config(page_title="GitHub OAuth Dashboard", page_icon="🐙")
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
                    "📷 Leitor RFID OCR"
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