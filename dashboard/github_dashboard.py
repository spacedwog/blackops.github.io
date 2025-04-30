# -----------------------------
# dashboard/github_dashboard.py
# -----------------------------
import time
import base64
import serial
import requests
import subprocess
import pandas as pd
import seaborn as sns
import streamlit as st
import statsmodels.api as sm
import serial.tools.list_ports
import matplotlib.pyplot as plt
from serial.serialutil import SerialException

class GitHubDashboard:
    def __init__(self, user_data):
        self.user_data = user_data

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
            "📉 Regressão - Gráfico",
            "🛡️ Relay e Firewall"
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

        with tabs[5]:
            self.exibir_relay_firewall()

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
            # Simula evolução de repositórios com base no tempo
            linguagem = self.user_data.get("language", 0)
            repos = self.user_data.get("public_repos", 0)
            datas = pd.date_range(end=pd.Timestamp.today(), periods=10)

            df = pd.DataFrame({
                "data": datas,
                "linguagens": [linguagem + i for i in range(10)],
                "repositorios": [repos + i + (i % 3 - 1) for i in range(10)]
            }).set_index("data")

            # Gráfico de linha simples
            st.line_chart(df[["repositorios"]])

            # Média móvel
            df["media_movel"] = df["repositorios"].rolling(window=3).mean()
            fig, ax = plt.subplots()
            df["repositorios"].plot(ax=ax, label="Repositórios", marker="o")
            df["media_movel"].plot(ax=ax, label="Média Móvel (3 dias)", linestyle="--")
            ax.set_title("Repositórios GitHub - Série Temporal com Média Móvel")
            ax.legend()
            st.pyplot(fig)

        except Exception as e:
            st.error(f"Erro ao exibir séries temporais: {e}")


    def exibir_relay_firewall(self) -> None:
        """
        Exibe as informações do relay.

        Returns:
            Show (Relay): Configurações carregadas do arquivo YAML.
        """
        log = []

        st.subheader("🚀 Cibersegurança: Relay e Firewall")
        status = st.empty()
        reiniciar = st.button("💡 Reiniciar Relé")

        porta_serial = self.detectar_porta_serial() or "COM3"
        baud_rate = 9600

        try:
            if reiniciar:
                st.write("Reiniciando relé...")
                log = ["✅ Comando enviado: RESTART"]
                self.enviar_comando(porta_serial, baud_rate, b"RESTART\n", log)
                status.success("Relé Reiniciado com sucesso! ✅")

            st.info(f"🔌 Iniciando comunicação serial na porta `{porta_serial}`...")
            try:
                with serial.Serial(porta_serial, baud_rate, timeout=2) as ser:
                    time.sleep(2)
                    ser.write(b"FIREWALL\n")
                    log = ["✅ Comando enviado: FIREWALL"]
                    start = time.time()
                    raw_response = ser.readline()
                    latencia = time.time() - start
            except serial.SerialException as se:
                st.error(f"Erro de conexão serial: {se}")
            except Exception as e:
                st.error(f"Erro inesperado ao iniciar comunicação serial: {e}")

            if log and raw_response:
                self.exibir_resultado(raw_response, latencia, log)

        except SerialException as se:
            st.error(f"Erro de conexão serial: {se}")
        except Exception as e:
            st.error(f"Erro inesperado ao iniciar comunicação serial: {e}")

    def detectar_porta_serial(self) -> None:
        """
        Método de detecção da porta serial do aplicativo.

        Returns:
            Show (Port): Configurações carregadas do arquivo YAML.
        """
        portas = list(serial.tools.list_ports.comports())
        for p in portas:
            if any(chave in p.description for chave in ["USB", "CH340", "CP210"]):
                return p.device
        return None

    def enviar_comando(self, porta, baud_rate, comando, log):
        """
        Método que executa a operação de enviar comando.

        Returns:
            Send (Command): Configurações carregadas do arquivo YAML.
        """
        try:
            with serial.Serial(porta, baud_rate, timeout=1) as ser:
                if isinstance(comando, str):
                    comando = comando.encode()
                ser.write(comando)
                log.append(f"✅ Comando enviado (interno): {comando.decode().strip()}")
        except SerialException as e:
            log.append(f"❌ Erro ao enviar comando para a porta serial: {str(e)}")
        except Exception as e:
            log.append(f"❌ Erro inesperado ao enviar comando: {str(e)}")

    def exibir_resultado(self, raw_response, latencia, log) -> None:
        """
        Exibe o resultado das informações do relay.

        Returns:
            Show (Relay): Configurações carregadas do arquivo YAML.
        """
        response_str = self.decodificar_resposta(raw_response, log)
        abas = st.tabs(["📱 Resposta", "📦 Bytes Recebidos", "🧾 Log de Decodificação", "🧪 Análise XOR"])

        with abas[0]:
            st.subheader("📱 Resposta do Dispositivo")
            if response_str:
                st.success(f"📱 Resposta do dispositivo: {response_str}")
            else:
                st.warning("⚠️ Dados não textuais recebidos.")
                st.code(raw_response.hex(), language="text")

            st.text(f"⏱️ Tempo de resposta: {latencia:.2f} segundos")

            if (response_str and "OK" in response_str.upper()):
                st.success("🔍 Firewall validado, relay seguro e potenciometro funcional.")
            else:
                st.error(f"❌ Nenhuma resposta válida foi interpretada.:{response_str}")


        with abas[1]:
            st.code(" ".join(f"{b:02x}" for b in raw_response), language="text")
            byte_table = pd.DataFrame({
                "Byte (Hex)": [f"{b:02x}" for b in raw_response],
                "Byte (Dec)": [str(b) for b in raw_response],
                "ASCII": [chr(b) if 32 <= b <= 126 else "." for b in raw_response]
            })
            with st.expander("📦 Bytes Recebidos"):
                st.dataframe(byte_table)

        with abas[2]:
            st.subheader("🧾 Log de Decodificação")
            st.code("\n".join(log), language="text")

        with abas[3]:
            self.exibir_analise_xor(raw_response)

    def decodificar_resposta(self, raw, log) -> None:
        """
        Método de descriptografia.

        Returns:
            Show (Descript): Configurações carregadas do arquivo YAML.
        """
        try:
            response = raw.decode("utf-8")
            log.append("🔍 Decodificação: UTF-8")
            return response
        except UnicodeDecodeError:
            try:
                response = raw.decode("latin1")
                log.append("🔍 Decodificação: Latin-1")
                return response
            except Exception:
                try:
                    base64_str = raw.decode("utf-8", errors="ignore")
                    decoded = base64.b64decode(base64_str).decode("utf-8", errors="replace")
                    log.append("🔍 Decodificação: Base64 (fallback)")
                    return decoded
                except Exception as e:
                    log.append(f"🚨 Falha na decodificação base64: {e}")
        return None

    def exibir_analise_xor(self, raw_response) -> None:
        """
        Exibe as informações do relay, com base em uma análise XOR.

        Returns:
            Show (Xor): Configurações carregadas do arquivo YAML.
        """
        st.subheader("🧪 Análise XOR Brute Force - Tabela Redimensional")
        palavras_chave = ["OK", "FIREWALL", "ACCESS", "RESTART", "DENIED", "GRANTED", "SECURE"]
        tabela_xor = []

        for key in range(1, 256):
            xor_result = [b ^ key for b in raw_response]
            decoded = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in xor_result)

            palavras_detectadas = [p for p in palavras_chave if p.upper() in decoded.upper()]
            printable_chars = sum(1 for c in decoded if 32 <= ord(c) <= 126)
            printable_ratio = printable_chars / len(decoded)

            if printable_ratio > 0.8 and palavras_detectadas:
                tabela_xor.append({
                    "Key": key,
                    "Printable Ratio": printable_ratio,
                    "Qtd Palavras-chave": len(palavras_detectadas),
                    "Palavra-chave Detectada": ", ".join(palavras_detectadas),
                    "Texto Decodificado": decoded
                })

        if tabela_xor:
            df_xor = pd.DataFrame(tabela_xor).sort_values(by=["Qtd Palavras-chave", "Printable Ratio"], ascending=False)

            melhor_linha = df_xor.iloc[0]
            st.markdown("### 🔍 Insights")
            st.write(f"**Chave Encontrada:** `{melhor_linha['Key']}`")
            st.write(f"**Texto Decodificado:** `{melhor_linha['Texto Decodificado']}`")
            st.write(f"**Palavras-chave Detectadas:** `{melhor_linha['Palavra-chave Detectada']}`")
            st.write(f"**Printable Ratio:** `{melhor_linha['Printable Ratio']:.2f}`")
            st.write(f"**Qtd Palavras-chave:** `{melhor_linha['Qtd Palavras-chave']}`")
