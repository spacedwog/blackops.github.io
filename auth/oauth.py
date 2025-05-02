# -----------------------------
# auth/oauth.py
# -----------------------------
import jwt
import time
import socket
import requests
import subprocess
import dns.resolver
import streamlit as st
from urllib.parse import urlencode
from datetime import datetime, timedelta, timezone
from dashboard.github_dashboard import GitHubDashboard
from config.firewall_inspector import FirewallInspector
from config.settings import OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET, REDIRECT_URI

class OAuthGitHub:
    AUTH_URL = "https://github.com/login/oauth/authorize"
    TOKEN_URL = "https://github.com/login/oauth/access_token"
    USER_API_URL = "https://api.github.com/user"

    @classmethod
    def login_button(cls):
        # sourcery skip: use-fstring-for-concatenation
        # sourcery skip: merge-nested-ifs
        if "access_token" not in st.session_state:
            if st.button("🔐 Login com GitHub"):
                if "code" not in st.query_params:
                    params = {
                        "client_id": OAUTH_CLIENT_ID,
                        "redirect_uri": REDIRECT_URI,
                        "scope": "read:user user:email",
                        "state": "secure_random_string"
                    }
                    auth_url = cls.AUTH_URL + "?" + urlencode(params)
                    
                    st.markdown("[Redirecionando... clique aqui se não for automático](" + auth_url + ")")
                    st.markdown(
                        """<meta http-equiv="refresh" content="0;URL='""" + auth_url + """'" />""",
                        unsafe_allow_html=True
                    )
                    
                    

    @classmethod
    def login_github_app(cls, app_id, private_key_pem, installation_id):
        """Autenticação via GitHub App: gera token de instalação."""
        try:
            now = datetime.now(timezone.utc)
            payload = {
                "iat": int(now.timestamp()),
                "exp": int((now + timedelta(minutes=10)).timestamp()),
                "iss": app_id
            }

            jwt_token = jwt.encode(payload, private_key_pem, algorithm="RS256")

            # Autentica como o App usando JWT
            headers = {
                "Authorization": f"Bearer {jwt_token}",
                "Accept": "application/vnd.github+json"
            }

            url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
            response = requests.post(url, headers=headers)

            if response.status_code == 201:
                access_token = response.json()["token"]
                st.session_state["access_token"] = access_token
                st.session_state["tokken_expiry"] = time.time() + 3600
                st.success("✅ Autenticado com GitHub App.")
                return access_token
            else:
                st.error(f"Erro ao gerar token de instalação: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            st.error(f"Erro na autenticação do GitHub App: {str(e)}")
            return None

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
    def get_user_from_token(cls):  # sourcery skip: use-fstring-for-concatenation
        token = st.session_state.get("access_token")
        expiry = st.session_state.get("tokken_expiry")

        if not token or time.time() > expiry:
            # Token ausente ou expirado
            st.session_state.pop("access_token", None)
            st.session_state.pop("token_expiry", None)
            st.warning("⚠️ Sessão expirada. Redirecionando para login...")
            cls.login_button()  # força re-login
            st.stop()

        headers = {"Authorization": "Bearer " + token}
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
        # sourcery skip: use-named-expression
        """Renderiza o dashboard após autenticação GitHub."""
        user_data = cls.get_user_from_token()
        if user_data:
            dashboard = GitHubDashboard(user_data)
            dashboard.exibir_perfil()
            dashboard.exibir_lista_repositorios()
            dashboard.exibir_data_science()
            dashboard.exibir_relay_firewall()
        else:
            st.warning("⚠️ Faça login com o GitHub para acessar seu dashboard.")

    # 🔐 CIBERSEGURANÇA - NETWORK TRANSPORT + FIREWALL

    @classmethod
    def verificar_transporte_rede(cls):
        # sourcery skip: use-fstring-for-concatenation
        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            st.write("**Host:** " + hostname)
            st.write("**IP Local:** " + ip_address)
        except Exception as e:
            st.error("Erro ao obter informações de rede: " + str(e))

    @classmethod
    def verificar_dns(cls, dominio="github.com"):
        # sourcery skip: use-fstring-for-concatenation
        try:
            resolver = dns.resolver.Resolver()
            resolver.timeout = 2.0
            resolver.lifetime = 5.0
            resolver.nameservers = ['8.8.8.8', '1.1.1.1']
            resposta = resolver.resolve(dominio, 'A')
            ips = [ip.to_text() for ip in resposta]
            st.write("**DNS (" + dominio + "):** " + ", ".join(ips))
        except Exception as e:
            st.error("Erro ao resolver DNS: " + str(e))

    @classmethod
    def verificar_porta(cls, host="github.com", porta=443):
        # sourcery skip: use-fstring-for-concatenation
        try:
            with socket.create_connection((host, porta), timeout=3) as sock:
                st.success("Porta " + str(porta) + " aberta em " + host)
        except Exception:
            st.error("Porta " + str(porta) + " fechada ou inacessível em " + host)

    @classmethod
    def exibir_cyberseguranca(cls):
        # sourcery skip: use-fstring-for-concatenation
        st.subheader("🛡️ Cibersegurança: Relatório de Segurança")
                
        cls.verificar_transporte_rede()
        cls.verificar_dns()
        cls.verificar_porta()
        FirewallInspector.verificar_firewall()
        FirewallInspector.listar_conexoes()