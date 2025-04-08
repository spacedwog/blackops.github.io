import streamlit as st
from auth.blackboard import BlackboardValidator
from auth.oauth import OAuthGitHub
from dashboard.github_dashboard import GitHubDashboard
from database.db import UsuarioDB

class GitHubDashboardApp:
    def __init__(self):
        self.db = UsuarioDB()
        self.auth = OAuthGitHub()
        self.validator = BlackboardValidator()
        self.user_data = None

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
                    "🛡️ Cibersegurança"
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