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

    def ler_rfid_via_camera(self):
        st.info("📷 Posicione o cartão RFID com código visível.")

        if st.button("🔍 Escanear Cartão RFID"):
            imagem = self.capturar_imagem_camera(duracao=5)

            if imagem is not None:
                uid_detectado = self.extrair_uid_da_imagem(imagem)

                if uid_detectado:
                    self.processar_uid_detectado(uid_detectado)
                else:
                    st.error("❌ Não foi possível reconhecer o texto do cartão.")
            else:
                st.error("❌ Falha ao capturar imagem da câmera.")

    def capturar_imagem_camera(self, duracao=5):
        cap = cv2.VideoCapture(0)

        # ✅ Configurar resolução HD
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        st_frame = st.empty()
        frame = None
        start_time = time.time()

        altura_linha = 0
        direcao = 1  # 1 para baixo, -1 para cima

        while time.time() - start_time < duracao:
            ret, frame = cap.read()
            if not ret:
                continue

            # Criar uma cópia da imagem para desenhar a linha de scanner
            frame_com_linha = frame.copy()
            altura, largura, _ = frame.shape

            # Desenhar a linha verde de scanner
            cv2.line(frame_com_linha, (0, altura_linha), (largura, altura_linha), (0, 255, 0), 2)

            # Atualizar posição da linha
            altura_linha += direcao * 10
            if altura_linha >= altura or altura_linha <= 0:
                direcao *= -1  # Inverter direção

            # Mostrar o frame com a linha no Streamlit
            st_frame.image(frame_com_linha, channels="BGR", caption="📡 Escaneando cartão...")

        cap.release()
        return frame
    
    def extrair_uid_da_imagem(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # ✅ Aplicar filtro de nitidez
        kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])
        sharpened = cv2.filter2D(gray, -1, kernel)

        # ✅ Aumentar contraste
        contrast = cv2.convertScaleAbs(sharpened, alpha=1.5, beta=0)

        _, thresh = cv2.threshold(contrast, 100, 255, cv2.THRESH_BINARY)

        config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEF'
        texto = pytesseract.image_to_string(thresh, config=config).strip().upper()
        return texto if texto else None
    
    def processar_uid_detectado(self, uid_detectado):
        st.success(f"✅ UID detectado: `{uid_detectado}`")
        usuario = self.db.get_usuario_por_uid(uid_detectado)

        if not usuario:
            st.info("🔒 Cartão não registrado. Registrando novo usuário.")
            nome = self.user_data.get("name")
            login_github = self.user_data.get("login")
            nivel = "Usuario"
            self.db.registrar_cartao(uid_detectado, nome, login_github, nivel)
            st.success("✅ Cartão registrado com sucesso!")
        else:
            self.exibir_dados_usuario(usuario)

            if usuario[2] == self.user_data.get("login"):
                self.executar_acesso_autenticado(usuario, uid_detectado)
            else:
                st.error("❌ Acesso negado: usuário inválido.")

    def exibir_dados_usuario(self, usuario):
        df = pd.DataFrame([{
            "Nome": usuario[1],
            "Login": usuario[2],
            "Nível": usuario[3],
            "Último Acesso": usuario[4]
        }])
        st.table(df)

    def executar_acesso_autenticado(self, usuario, uid_detectado):
        self.mensagem = f"✅ Bem-vindo, {usuario[3]} {usuario[2]}! Seu último acesso foi em {usuario[4]}"
        st.success(self.mensagem)

        try:
            comando = "./executar_blackops.ps1"
            resultado = subprocess.run(
                ["powershell", "-Command", comando],
                capture_output=True,
                text=True,
                shell=True
            )
            st.code(resultado.stdout or resultado.stderr)
        except Exception as e:
            st.error(f"Erro ao executar: {e}")

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