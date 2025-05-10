# -----------------------------
# auth/oauth.py
# -----------------------------
import time
import socket
import requests
import subprocess
import dns.resolver
import streamlit as st
from urllib.parse import urlencode
from dashboard.github_dashboard import GitHubDashboard
from config.firewall_inspector import FirewallInspector
from config.settings import OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET, REDIRECT_URI

class OAuthGitHub:
    AUTH_URL = "https://github.com/login/oauth/authorize"
    TOKEN_URL = "https://github.com/login/oauth/access_token"
    USER_API_URL = "https://api.github.com/user"
    
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.access_token = None  # Certifique-se de que será atualizado após login
        
    @classmethod
    def login_button(cls):
        # Layout tech visual com HTML + CSS embutido
        st.markdown("""
            <style>
            .tech-button {
                background: linear-gradient(135deg, #1f1f1f, #0f0f0f);
                color: #00ffe7;
                border: 1px solid #00ffe7;
                border-radius: 10px;
                padding: 1em 2em;
                font-size: 16px;
                font-family: 'Courier New', monospace;
                text-align: center;
                cursor: pointer;
                transition: all 0.3s ease-in-out;
            }
            .tech-button:hover {
                background: #00ffe7;
                color: #0f0f0f;
                box-shadow: 0 0 10px #00ffe7;
            }
            </style>
        """, unsafe_allow_html=True)

        if "access_token" not in st.session_state:
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                if st.button("🔐 Blackops(Login)", key="github_login", help="Clique para autenticar com GitHub"):
                    if "code" not in st.query_params:
                        params = {
                            "client_id": OAUTH_CLIENT_ID,
                            "redirect_uri": REDIRECT_URI,
                            "scope": "read:user user:email",
                            "state": "secure_random_string"
                        }
                        auth_url = cls.AUTH_URL + "?" + urlencode(params)
                        
                        st.markdown("<p class='tech-button'>Redirecionando para o GitHub...</p>", unsafe_allow_html=True)
                        st.markdown(
                            f"""<meta http-equiv="refresh" content="0;URL='{auth_url}'" />""",
                            unsafe_allow_html=True
                        )
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
        st.markdown("""
            <style>
            .cyber-box {
                background-color: #111827;
                border: 1px solid #00ffe7;
                border-radius: 12px;
                padding: 1em;
                color: #00ffe7;
                font-family: 'Courier New', monospace;
                box-shadow: 0 0 8px #00ffe7;
            }
            </style>
        """, unsafe_allow_html=True)

        st.markdown("<div class='cyber-box'><h3>🛡️ Cibersegurança: Relatório de Segurança</h3>", unsafe_allow_html=True)
 
        cls.verificar_transporte_rede()
        cls.verificar_dns()
        cls.verificar_porta()
        FirewallInspector.verificar_firewall()
        FirewallInspector.listar_conexoes()

        st.markdown("</div>", unsafe_allow_html=True)

    def coletar_dados_github(self, username):
        # sourcery skip: inline-immediately-returned-variable
        self.access_token = st.session_state.get("access_token")
        headers = {"Authorization": f"token {self.access_token}"} if self.access_token else {}
        user_url = f"{self.base_url}/users/{username}"
        repos_url = f"{self.base_url}/users/{username}/repos"

        user_data = requests.get(user_url, headers=headers).json()
        repos_data = requests.get(repos_url, headers=headers).json()

        dados = {
            "login": user_data.get("login"),
            "nome": user_data.get("name"),
            "bio": user_data.get("bio"),
            "localizacao": user_data.get("location"),
            "public_repos": user_data.get("public_repos"),
            "seguidores": user_data.get("followers"),
            "repositorios": [
                {
                    "nome": repo["name"],
                    "descricao": repo.get("description"),
                    "url": repo["html_url"],
                    "estrelas": repo["stargazers_count"]
                } for repo in repos_data
            ]
        }

        return dados