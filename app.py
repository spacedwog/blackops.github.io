# -----------------------------
# ./app.py
# -----------------------------
import time
import serial
import pickle
import joblib
import platform
import streamlit as st
from database.db import UsuarioDB
from auth.oauth import OAuthGitHub
from config.firewall import Firewall
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score
from auth.blackboard import BlackboardValidator
from sklearn.linear_model import LogisticRegression
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
        
    def firewall(self, modelo):
        # Firewall para autenticação de variáveis
        firewall = Firewall()
        chave_usuario = st.text_input("🔐 Chave de acesso (ex: secret123)")
        destino_nome = "modelo_autenticado"
        firewall.registrar_autorizacao(destino_nome, "secret123")  # chave válida predefinida

        variaveis_transmissao = {}

        if st.button("🚀 Transferir modelo via Firewall"):
            sucesso = firewall.transferir(modelo, destino_nome, variaveis_transmissao, chave_usuario)
            if sucesso:
                st.success("✅ Modelo transferido com sucesso para variável protegida!")
            else:
                st.error("❌ Acesso negado! Chave incorreta ou sem permissão.")

            if destino_nome in variaveis_transmissao:
                st.write("🔎 Modelo disponível na variável protegida. Exemplo de predição:")
                pred = variaveis_transmissao[destino_nome].predict([[5.1, 3.5, 1.4, 0.2]])
                st.write(f"🔮 Predição: {pred}")
                
    def salvar_arquivo(self, diretorio, modelo, nome_arquivo):
        # Botão para salvar
        if st.button("💾 Salvar modelo localmente"):
            try:
                os.makedirs(diretorio, exist_ok=True)
                caminho_completo = os.path.join(diretorio, nome_arquivo)
                joblib.dump(modelo, caminho_completo)
                st.success(f"✅ Modelo salvo com sucesso em: {caminho_completo}")
            except Exception as e:
                st.error(f"❌ Erro ao salvar o modelo: {e}")
                
    def carregar_arquivo(self, diretorio, nome_arquivo):
        caminho = os.path.join(diretorio, nome_arquivo)

        if not os.path.exists(caminho):
            st.error("❌ Arquivo não encontrado.")
            return None

        if st.button("📂 Carregar modelo salvo"):
            try:
                modelo_carregado = joblib.load(caminho)
                st.success("✅ Modelo carregado com sucesso via joblib!")
            except Exception as e_joblib:
                st.warning("⚠️ Falha ao carregar com joblib. Tentando com pickle...")

                try:
                    with open(caminho, 'rb') as f:
                        modelo_carregado = pickle.load(f)
                    st.success("✅ Modelo carregado com sucesso via pickle!")
                except Exception as e_pickle:
                    st.error("❌ Falha com joblib e pickle. O arquivo está corrompido.")
                    st.error(f"Erro: {e_pickle}")
                    try:
                        os.remove(caminho)
                        st.warning("🚮 Arquivo corrompido foi removido automaticamente.")
                    except Exception as e_remover:
                        st.error(f"❌ Erro ao tentar remover o arquivo: {e_remover}")
                    return None

            # Predição de exemplo
            try:
                st.write("Exemplo de predição com entrada [5.1, 3.5, 1.4, 0.2]:")
                pred = modelo_carregado.predict([[5.1, 3.5, 1.4, 0.2]])
                st.write(f"🔮 Predição: {pred}")
            except Exception as e_pred:
                st.error(f"❌ Erro ao realizar predição: {e_pred}")

            return modelo_carregado
    
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
                    st.title("🤖 Cyber-Brain: Inteligência Artificial na Nuvem")
                    st.header("🧠 Transferência Segura de Conhecimento com Firewall")

                    # Entradas do usuário
                    diretorio = st.text_input("Diretório para salvar", "./modelos_salvos")
                    nome_arquivo = st.text_input("Nome do arquivo", "modelo_iris.joblib")

                    # Carrega e separa os dados
                    iris = load_iris()
                    X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.2)

                    # Treina o modelo
                    modelo = LogisticRegression(max_iter=200)
                    modelo.fit(X_train, y_train)
                    
                    self.firewall(modelo)
                    self.salvar_arquivo(diretorio, modelo, nome_arquivo)
                    self.carregar_arquivo(diretorio, nome_arquivo)

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