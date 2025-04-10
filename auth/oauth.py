import time
import socket
import requests
import dns.resolver
import streamlit as st
from urllib.parse import urlencode
from config.settings import OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET, REDIRECT_URI
from dashboard.github_dashboard import GitHubDashboard  # Certifique-se de que este caminho está correto

class OAuthGitHub:
    AUTH_URL = "https://github.com/login/oauth/authorize"
    TOKEN_URL = "https://github.com/login/oauth/access_token"
    USER_API_URL = "https://api.github.com/user"

    @classmethod
    def login_button(cls):
        if "access_token" not in st.session_state:
            if st.button("🔐 Login com GitHub"):
                if "code" not in st.query_params:
                    params = {
                        "client_id": OAUTH_CLIENT_ID,
                        "redirect_uri": REDIRECT_URI,
                        "scope": "read:user user:email",
                        "state": "secure_random_string"
                    }
                    auth_url = f"{cls.AUTH_URL}?{urlencode(params)}"
                    st.markdown(f"[🔗 Redirecionando... clique aqui se não for automático]({auth_url})")
                    st.markdown(
                        f"""<meta http-equiv="refresh" content="0;URL='{auth_url}'" />""",
                        unsafe_allow_html=True
                    )

    @classmethod
    def callback(cls):
        query_params = st.query_params
        code = query_params.get("code")

        if not code:
            return None

        data = {
            "client_id": OAUTH_CLIENT_ID,
            "client_secret": OAUTH_CLIENT_SECRET,
            "code": code,
            "redirect_uri": REDIRECT_URI
        }

        headers = {"Accept": "application/json"}
        response = requests.post(cls.TOKEN_URL, data=data, headers=headers)
        token_json = response.json()
        access_token = token_json.get("access_token")

        if not access_token:
            st.error("❌ Erro ao obter token de acesso do GitHub.")
            return None

        st.session_state["access_token"] = access_token
        st.session_state["tokken_expiry"] = time.time() + 3600
        return cls.get_user_from_token()

    @classmethod
    def get_user_from_token(cls):
        token = st.session_state.get("access_token")
        expiry = st.session_state.get("tokken_expiry")

        if not token or time.time() > expiry:
            # Token ausente ou expirado
            st.session_state.pop("access_token", None)
            st.session_state.pop("token_expiry", None)
            st.warning("⚠️ Sessão expirada. Redirecionando para login...")
            cls.login_button()  # força re-login
            st.stop()

        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(cls.USER_API_URL, headers=headers)

        if response.status_code != 200:
            st.warning("⚠️ Token inválido ou expirado. Refaça o login.")
            st.session_state.pop("access_token", None)
            st.session_state.pop("token_expiry", None)
            cls.login_button()
            st.stop()

        st.query_params.clear()
        return response.json()

    @classmethod
    def exibir_dashboard_github(cls):
        """Renderiza o dashboard após autenticação GitHub."""
        user_data = cls.get_user_from_token()
        if user_data:
            dashboard = GitHubDashboard(user_data)
            dashboard.exibir_perfil()
            dashboard.exibir_lista_repositorios()
            dashboard.exibir_regressao_info()
            dashboard.exibir_regressao_plot()
            dashboard.exibir_relay_firewall()
        else:
            st.warning("⚠️ Faça login com o GitHub para acessar seu dashboard.")

    # 🔐 CIBERSEGURANÇA - NETWORK TRANSPORT + FIREWALL

    @classmethod
    def verificar_transporte_rede(cls):
        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            st.write(f"**Host:** {hostname}")
            st.write(f"**IP Local:** {ip_address}")
        except Exception as e:
            st.error(f"Erro ao obter informações de rede: {e}")

    @classmethod
    def verificar_dns(cls, dominio="github.com"):
        try:
            resposta = dns.resolver.resolve(dominio, 'A')
            ips = [ip.to_text() for ip in resposta]
            st.write(f"**DNS ({dominio}):** {', '.join(ips)}")
        except Exception as e:
            st.error(f"Erro ao resolver DNS: {e}")

    @classmethod
    def verificar_porta(cls, host="github.com", porta=443):
        try:
            with socket.create_connection((host, porta), timeout=3) as sock:
                st.success(f"✅ Porta {porta} aberta em {host}")
        except Exception:
            st.error(f"❌ Porta {porta} fechada ou inacessível em {host}")

    @classmethod
    def verificar_firewall(cls):
        try:
            regras = {
                "HTTPS": True,
                "HTTP": False,
                "SSH": False
            }
            st.write("**Regras do Firewall (Simulado):**")
            for servico, permitido in regras.items():
                status = "✅ Permitido" if permitido else "⛔ Bloqueado"
                st.write(f"• {servico}: {status}")
        except Exception as e:
            st.error(f"Erro ao verificar firewall: {e}")

    @classmethod
    def exibir_cyberseguranca(cls):
        st.subheader("🛡️ Cibersegurança: Relatório de Segurança")
        cls.verificar_transporte_rede()
        cls.verificar_dns()
        cls.verificar_porta()
        cls.verificar_firewall()