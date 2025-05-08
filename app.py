# -----------------------------
# ./app.py
# -----------------------------
import platform
import streamlit as st
from framework.app import App
from database.db import UsuarioDB
from auth.oauth import OAuthGitHub
from config.firewall import Firewall
from sklearn.datasets import load_iris
from auth.blackboard import BlackboardValidator
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from dashboard.github_dashboard import GitHubDashboard
from config.firewall_relay_controller import FirewallRelayController

# OCR e imagem
import os
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
        self.framework = App()
        self.auth = OAuthGitHub()
        self.blackboard = BlackboardValidator()
        self.user_data = None
    
    def run(self):
        # sourcery skip: extract-duplicate-method, extract-method, remove-redundant-fstring
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
                st.toast("⚫ Blackops(Relay/Firewall/Cibersegurança)")
                self.dashboard = GitHubDashboard(self.user_data)
                abas = st.tabs([
                    "👤 Perfil",
                    "📦 Repositórios",
                    "📈 Data Science",
                    "🧱 Firewall",
                    "📟 Framework",
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
                    st.title("🧱 Firewall: Verificação de Status")
                    st.header("🔍 Verificar Firewall Relay")
                    
                    controller = FirewallRelayController(port="COM3")
                    st.write(controller.get_relay_status())
                    st.write(controller.detect_active_block_reasons())
                    st.write(controller.diagnose_common_block_reasons())

                    # Criação de um botão para verificar o status
                    if st.button("🔍 Verificar Firewall Relay"):# Ajuste conforme necessário
                        status = controller.get_firewall_status_and_control_relay()
                        st.write(status)
                        print("\n📋 Motivos possíveis:")
                        for reason in controller.list_possible_reasons():
                            st.write("-", reason)
                            
                with abas[4]:
                            
                    aba = st.tabs(["📜 Regras de Firewall", "📦 Simular Pacotes", "📁 Exportar/Importar(JSON)"])
                    
                    with aba[0]:
                        self.framework.render_rules_tab()
                    with aba[1]:
                        self.framework.render_packet_simulation_tab()
                    with aba[2]:
                        self.framework.render_import_export_tab()

                with abas[5]:
                    self.auth.exibir_cyberseguranca()

                with abas[6]:
                    st.title("🤖 Cyber-Brain: Inteligência Artificial na Nuvem")
                    st.header("🧠 Transferência Segura de Conhecimento com Firewall e GitHub")

                    st.markdown("Essa seção permite exportar dados do GitHub e modelos IA com verificação de firewall e segurança.")

                    # Entradas do usuário
                    diretorio = st.text_input("Diretório para salvar", "./modelos_salvos")
                    nome_arquivo = st.text_input("Nome do arquivo", "modelo_iris.joblib")
                    nome_repo = st.text_input("🔗 Nome do repositório GitHub (ex: user/repo)", "")

                    firewall = Firewall()

                    if st.button("🔄 Treinar e Exportar Modelo via Firewall"):
                        st.info("🔍 Verificando permissões do firewall...")

                        if firewall.autorizar_transferencia("modelo_ia"):
                            iris = load_iris()
                            X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.2)

                            modelo = LogisticRegression(max_iter=200)
                            modelo.fit(X_train, y_train)

                            resultado = firewall.transferir_via_firewall(modelo, diretorio, nome_arquivo)
                            st.success(f"✅ Modelo exportado com sucesso: {resultado}")
                        else:
                            st.error("❌ Transferência bloqueada pelo firewall. Ação não autorizada.")

                    if nome_repo and st.button("⬇️ Exportar Código/Repositório GitHub via Firewall"):
                        st.info(f"📡 Solicitando exportação segura do repositório `{nome_repo}`...")

                        if firewall.autorizar_transferencia("github_repo", recurso=nome_repo):
                            try:
                                caminho_zip = self.auth.exportar_repositorio_zip(nome_repo, destino=diretorio)
                                firewall.registrar_transferencia("github_repo", recurso=nome_repo)
                                st.success(f"📁 Repositório exportado com sucesso para: {caminho_zip}")
                            except Exception as e:
                                st.error(f"Erro ao exportar repositório: {str(e)}")
                        else:
                            st.error("🚫 Exportação bloqueada pelo firewall. Permissão negada.")

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