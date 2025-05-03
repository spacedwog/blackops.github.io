# -----------------------------
# ./app.py
# -----------------------------
import time
import boto3
import serial
import joblib
import platform
import streamlit as st
from database.db import UsuarioDB
from auth.oauth import OAuthGitHub
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score
from auth.blackboard import BlackboardValidator
from botocore.exceptions import NoCredentialsError
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
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
                    "🔄 Cyber-Brain"
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
                    st.header("🔄 Cyber-Brain: Machine Learning + Nuvem")

                    if st.button("🚀 Treinar Modelo de IA"):
                        # Carregar dados
                        iris = load_iris()
                        X_train, X_test, y_train, y_test = train_test_split(
                            iris.data, iris.target, test_size=0.3, random_state=42
                        )

                        # Criar e treinar modelo
                        modelo = RandomForestClassifier(n_estimators=100, random_state=42)
                        modelo.fit(X_train, y_train)
                        y_pred = modelo.predict(X_test)

                        # Avaliar e exibir acurácia
                        acc = accuracy_score(y_test, y_pred)
                        st.success(f"✅ Modelo treinado com acurácia: {acc:.2%}")

                        # Salvar modelo localmente
                        nome_modelo = 'modelo_iris.joblib'
                        joblib.dump(modelo, nome_modelo)
                        st.info("📁 Modelo salvo localmente como 'modelo_iris.joblib'.")

                        # Upload para AWS S3
                        def upload_para_s3(arquivo_local, nome_bucket, nome_s3):
                            s3 = boto3.client('s3')
                            try:
                                s3.upload_file(arquivo_local, nome_bucket, nome_s3)
                                st.success(f"☁️ Upload concluído: s3://{nome_bucket}/{nome_s3}")
                            except FileNotFoundError:
                                st.error("❌ Arquivo não encontrado.")
                            except NoCredentialsError:
                                st.error("❌ Credenciais AWS não configuradas.")

                        # Formulário para upload
                        st.subheader("☁️ Enviar para AWS S3")
                        bucket = st.text_input("Nome do Bucket S3", "meu-bucket-modelos")
                        nome_s3 = st.text_input("Caminho no S3", "modelos/modelo_iris.joblib")

                        if st.button("📤 Enviar para o S3"):
                            upload_para_s3(nome_modelo, bucket, nome_s3)

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