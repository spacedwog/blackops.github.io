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
            df = pd.DataFrame({
                "linguagens": [linguagem + i for i in range(-5, 5)],
                "repositorios": [repos + i for i in range(-5, 5)]
            })
            fig, ax = plt.subplots()
            sns.regplot(x="linguagens", y="repositorios", data=df, ax=ax)
            ax.set_title("Regressão Linear: Linguagens vs Repositórios (Baseada no seu GitHub)")
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Erro ao exibir gráfico de regressão: {e}")

    def exibir_series_temporais(self) -> None:
        """
        Método DataScience.

        Returns:
            Show (Temporais): Configurações carregadas do arquivo YAML.
        """
        st.subheader("📊 Análise de Séries Temporais com seus dados do GitHub")
        try:
            linguagem = self.user_data.get("language", 0)
            repos = self.user_data.get("public_repos", 0)
            datas = pd.date_range(end=pd.Timestamp.today(), periods=10)

            df = pd.DataFrame({
                "data": datas,
                "linguagens": [linguagem + i for i in range(10)],
                "repositorios": [repos + i + (i % 3 - 1) for i in range(10)]
            }).set_index("data")

            # Gráfico Altair com datas convertidas para string
            df_plot = df.reset_index()
            df_plot["data"] = df_plot["data"].astype(str)
            st.altair_chart(df_plot[["data", "repositorios"]], use_container_width=True)

            # Média móvel com Matplotlib
            df["media_movel"] = df["repositorios"].rolling(window=3).mean()
            fig, ax = plt.subplots()
            df["repositorios"].plot(ax=ax, label="Repositórios", marker="o")
            df["media_movel"].plot(ax=ax, label="Média Móvel (3 dias)", linestyle="--")
            ax.set_title("Repositórios GitHub - Série Temporal com Média Móvel")
            ax.legend()
            st.pyplot(fig)

        except Exception as e:
            st.error(f"Erro ao exibir séries temporais: {e}")
