# -----------------------------
# dashboard/github_dashboard.py
# -----------------------------
import requests
import pandas as pd
import seaborn as sns
import streamlit as st
import statsmodels.api as sm
import matplotlib.pyplot as plt

class GitHubDashboard:
    def __init__(self, user_data):
        self.user_data = user_data
        self.serial_relay = None
        self.porta_serial = "COM3"
        self.baud_rate = 9600
        self.raw_response = None
        self.latencia = None
        self.log = []

    def show_dashboard(self) -> None:
        """
        Exibe a lista de funcionalidades no aplicative.

        Returns:
            Show (None): Configurações carregadas do arquivo YAML.
        """
        tabs = st.tabs([
            "👤 Perfil",
            "📦 Repositórios Públicos",
            "🗃️ Lista Detalhada",
            "📊 Regressão - Info",
            "📉 Regressão - Gráfico"
        ])

        with tabs[0]:
            self.exibir_perfil()

        with tabs[1]:
            self.exibir_repositorios_publicos()

        with tabs[2]:
            self.exibir_lista_repositorios()

        with tabs[3]:
            self.exibir_data_science()

        with tabs[4]:
            self.exibir_data_science_plot()

    def exibir_perfil(self) -> None:
        """
        Exibe o perfil do usuário do github.

        Returns:
            Exibir (None): Configurações carregadas do arquivo YAML.
        """
        st.title("👤 GitHub Dashboard")
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(self.user_data.get("avatar_url"), width=120)
        with col2:
            st.subheader(self.user_data.get("name") or self.user_data.get("login"))
            st.caption(f"[🔗 {self.user_data.get('login')}]({self.user_data.get('html_url')})")
            if self.user_data.get("location"):
                st.text(f"📍 {self.user_data['location']}")
            if self.user_data.get("email"):
                st.text(f"📧 {self.user_data['email']}")
            if self.user_data.get("bio"):
                st.markdown(f"> _{self.user_data['bio']}_")

    def exibir_repositorios(self) -> None:
        """
        Exibe a lista de repositórios no aplicative.

        Returns:
            Show (None): Configurações carregadas do arquivo YAML.
        """
        aba1, aba2 = st.tabs(["📦 Repositórios Públicos", "🗃️ Lista Detalhada de Repositórios"])
        with aba1:
            self.exibir_repositorios_publicos()
        with aba2:
            self.exibir_lista_repositorios()

    def exibir_repositorios_publicos(self) -> None:
        """
        Exibe a lista de repositórios publicos no aplicative.

        Returns:
            Show (None): Configurações carregadas do arquivo YAML.
        """
        st.subheader("📦 Repositórios Públicos")
        repos_url = self.user_data.get("repos_url")
        if repos_url:
            response = requests.get(repos_url)
            if response.status_code == 200:
                repos = response.json()
                if isinstance(repos, list):
                    for repo in repos[:100]:
                        st.markdown(f"📔️ [{repo['name']}]({repo['html_url']}) — ⭐ {repo['stargazers_count']}")
                else:
                    st.warning("\u26a0\ufe0f Dados de repositórios inválidos recebidos da API.")
            else:
                st.error(f"❌ Erro ao acessar repositórios: {response.status_code}")

    def exibir_lista_repositorios(self) -> None:
        """
        Exibe a lista de repositórios detalhados no aplicative.

        Returns:
            Show (None): Configurações carregadas do arquivo YAML.
        """
        st.subheader("📃 Lista Detalhada de Repositórios")
        repos_url = self.user_data.get("repos_url")
        if repos_url:
            try:
                repos = requests.get(repos_url).json()
                df_repos = pd.DataFrame([{
                    "Nome": repo["name"],
                    "Descrição": repo.get("description", ""),
                    "Estrelas": repo["stargazers_count"],
                    "Forks": repo["forks_count"],
                    "URL": repo["html_url"],
                    "Linguagem": repo.get("language", "N/A"),
                    "Atualizado em": repo["updated_at"]
                } for repo in repos])
                st.dataframe(df_repos)
            except Exception as e:
                st.error(f"Erro ao carregar repositórios: {e}")
        else:
            st.warning("URL de repositórios não encontrada.")

    def exibir_data_science(self) -> None:
        """
        Exibe a lista de métodos datascience no aplicative.

        Returns:
            Show (None): Configurações carregadas do arquivo YAML.
        """
        aba1, aba2, aba3 = st.tabs([
            "📈 Data Science: Regression Table - Info",
            "📈 Data Science: Regression Table - Plot",
            "📊 Data Science: Séries Temporais"
        ])
        with aba1:
            self.exibir_data_science_resumo()
        with aba2:
            self.exibir_data_science_plot()
        with aba3:
            self.exibir_series_temporais()

    def exibir_data_science_resumo(self) -> None:
        """
        Método DataScience.

        Returns:
            Show (Resumo): Configurações carregadas do arquivo YAML.
        """
        st.subheader("📈 Data Science: Regression Table - Info")
        try:
            linguagem = self.user_data.get("language", 0)
            repos = self.user_data.get("public_repos", 0)
            df = pd.DataFrame({
                "linguagens": [linguagem + i for i in range(-5, 5)],
                "repositorios": [repos + i for i in range(-5, 5)]
            })
            X = df["linguagens"]
            y = df["repositorios"]
            X_const = sm.add_constant(X)
            modelo = sm.OLS(y, X_const).fit()
            st.write("**Resumo da Regressão Linear com seus dados do GitHub:**")
            st.text(modelo.summary())
        except Exception as e:
            st.error(f"Erro ao exibir regressão: {e}")

    def exibir_data_science_plot(self) -> None:
        """
        Método DataScience.

        Returns:
            Show (Plot): Configurações carregadas do arquivo YAML.
        """
        st.subheader("📈 Data Science: Regression Table - Plot")
        try:
            linguagem = self.user_data.get("language", 0)
            repos = self.user_data.get("public_repos", 0)
            # Criando DataFrame com dados simulados
            df = pd.DataFrame({
                "linguagens": [linguagem + i for i in range(-5, 5)],
                "repositorios": [repos + i for i in range(-5, 5)]
            })
            X = df["linguagens"]
            y = df["repositorios"]
            X_const = sm.add_constant(X)
            modelo = sm.OLS(y, X_const).fit()

            # Criando estrutura XML
            root = ET.Element("RegressaoLinear")
            entrada = ET.SubElement(root, "Entrada")
            usuario = ET.SubElement(entrada, "Usuario")
            ET.SubElement(usuario, "Linguagem").text = str(self.linguagem)
            ET.SubElement(usuario, "Repositorios").text = str(self.repositorios)

            dados = ET.SubElement(entrada, "Dados")
            for i in range(len(df)):
                obs = ET.SubElement(dados, "Observacao")
                ET.SubElement(obs, "Linguagens").text = str(df.iloc[i]["linguagens"])
                ET.SubElement(obs, "Repositorios").text = str(df.iloc[i]["repositorios"])

            modelo_elem = ET.SubElement(root, "Modelo")
            coefs = modelo.params
            pvalores = modelo.pvalues
            estatisticas = modelo_elem

            coef_elem = ET.SubElement(modelo_elem, "Coeficientes")
            ET.SubElement(coef_elem, "Constante").text = f"{coefs['const']:.4f}"
            ET.SubElement(coef_elem, "LinguaCoef").text = f"{coefs['linguagens']:.4f}"

            stats_elem = ET.SubElement(modelo_elem, "Estatisticas")
            ET.SubElement(stats_elem, "R2").text = f"{modelo.rsquared:.3f}"
            ET.SubElement(stats_elem, "PValorConstante").text = f"{pvalores['const']:.3f}"
            ET.SubElement(stats_elem, "PValorLingua").text = f"{pvalores['linguagens']:.3f}"
            ET.SubElement(stats_elem, "DesvioPadrao").text = f"{modelo.bse['linguagens']:.3f}"
            ET.SubElement(stats_elem, "FEstatistica").text = f"{modelo.fvalue:.2f}"

            # Adiciona o resumo textual como CDATA
            resumo_elem = ET.SubElement(root, "ResumoTexto")
            resumo_text = modelo.summary().as_text()
            cdata = ET.Comment(f"[CDATA[\n{resumo_text}\n]]")
            resumo_elem.append(cdata)

            # Converter para string
            xml_str = ET.tostring(root, encoding="unicode")
            return xml_str
        except Exception as e:
            st.error(f"Erro ao exibir regressão: {e}")
