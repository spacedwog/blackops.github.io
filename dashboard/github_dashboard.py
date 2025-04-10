import time
import base64
import serial
import requests
import pandas as pd
import seaborn as sns
import streamlit as st
from serial import Serial
import statsmodels.api as sm
import serial.tools.list_ports
import matplotlib.pyplot as plt


class GitHubDashboard:
    def __init__(self, user_data):
        self.user_data = user_data

    def show_dashboard(self):
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

    def exibir_perfil(self):
        aba1, aba2, aba3 = st.tabs(["👤 Perfil", "📦 Repositórios Públicos", "🗃️ Lista Detalhada de Repositórios"])
        with aba1:
            st.title("🔙 GitHub Dashboard")
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(self.user_data.get("avatar_url"), width=120)
            with col2:
                st.subheader(self.user_data.get("name") or self.user_data.get("login"))
                st.caption(f"[📍 {self.user_data.get('login')}]({self.user_data.get('html_url')})")
                if self.user_data.get("location"):
                    st.text(f"📍 {self.user_data['location']}")
                if self.user_data.get("email"):
                    st.text(f"📧 {self.user_data['email']}")
                if self.user_data.get("bio"):
                    st.markdown(f"> _{self.user_data['bio']}_")
        with aba2:
            self.exibir_repositorios_publicos()
        with aba3:
            self.exibir_lista_repositorios()

    def exibir_repositorios_publicos(self):
        st.subheader("📦 Repositórios Públicos")
        repos_url = self.user_data.get("repos_url")
        if repos_url:
            response = requests.get(repos_url)
            if response.status_code == 200:
                repos = response.json()
                if isinstance(repos, list):
                    for repo in repos[:100]:
                        st.markdown(f"🗄️ [{repo['name']}]({repo['html_url']}) — ⭐ {repo['stargazers_count']}")
                else:
                    st.warning("⚠️ Dados de repositórios inválidos recebidos da API.")
            else:
                st.error(f"❌ Erro ao acessar repositórios: {response.status_code}")

    def exibir_repositorios(self):
        st.subheader("📦 Repositórios")
        st.write("Selecione uma aba para exibir os repositórios.")
        
        aba1, aba2 = st.tabs(["📦 Repositórios Públicos", "🗃️ Lista Detalhada de Repositórios"])

        with aba1:
            self.exibir_repositorios_publicos()

        with aba2:
            self.exibir_lista_repositorios()
                

    def exibir_lista_repositorios(self):
        st.subheader("🗃️ Lista Detalhada de Repositórios")
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

    def exibir_data_science(self):
        aba1, aba2 = st.tabs(["📈 Data Science: Regression Table - Info", "📈 Data Science: Regression Table - Plot"])
        with aba1:
            self.exibir_data_science_resumo()
        with aba2:
            self.exibir_data_science_plot()

    def exibir_data_science_resumo(self):
        st.subheader("📈 Data Science: Regression Table - Info")
        try:
            repos = self.user_data.get("public_repos", 0)
            seguidores = self.user_data.get("followers", 0)
            df = pd.DataFrame({
                "repositorios": [repos + i for i in range(-5, 5)],
                "seguidores": [seguidores + i for i in range(-5, 5)]
            })
            X = df["repositorios"]
            y = df["seguidores"]
            X_const = sm.add_constant(X)
            modelo = sm.OLS(y, X_const).fit()
            st.write("**Resumo da Regressão Linear com seus dados do GitHub:**")
            st.text(modelo.summary())
        except Exception as e:
            st.error(f"Erro ao exibir regressão: {e}")

    def exibir_data_science_plot(self):
        st.subheader("📈 Data Science: Regression Table - Plot")
        try:
            repos = self.user_data.get("public_repos", 0)
            seguidores = self.user_data.get("followers", 0)
            df = pd.DataFrame({
                "repositorios": [repos + i for i in range(-5, 5)],
                "seguidores": [seguidores + i for i in range(-5, 5)]
            })
            fig, ax = plt.subplots()
            sns.regplot(x="repositorios", y="seguidores", data=df, ax=ax)
            ax.set_title("Regressão Linear: Repositórios vs Seguidores (Baseada no seu GitHub)")
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Erro ao exibir gráfico de regressão: {e}")

    def exibir_relay_firewall(self):
        log = []

        st.subheader("🚀 Cibersegurança: Relay e Firewall")
        status = st.empty()
        reiniciar = st.button("💡 Reiniciar Relé")

        porta_serial = self.detectar_porta_serial() or "COM4"
        baud_rate = 9600

        try:
            if reiniciar:
                st.write("Reiniciando relé...")
                log = ["✅ Comando enviado: RESTART"]
                self.enviar_comando(porta_serial, baud_rate, b"RESTART\n", log)
                status.success("Relé Reiniciado com sucesso! ✅")

            st.info(f"🔌 Iniciando comunicação serial na porta `{porta_serial}`...")
            with serial.Serial(porta_serial, baud_rate, timeout=2) as ser:
                time.sleep(2)
                ser.write(b"FIREWALL\n")
                log = ["✅ Comando enviado: FIREWALL"]
                start = time.time()
                raw_response = ser.readline()
                latencia = time.time() - start

            if log:
                self.exibir_resultado(raw_response, latencia, log)

        except serial.SerialException as se:
            st.error(f"Erro de conexão serial: {se}")
        except Exception as e:
            st.error(f"Erro inesperado: {e}")

    def detectar_porta_serial(self):
        portas = list(serial.tools.list_ports.comports())
        for p in portas:
            if any(chave in p.description for chave in ["USB", "CH340", "CP210"]):
                return p.device
        return None

    def enviar_comando(self, porta, baud_rate, comando, log):
        try:
            with serial.Serial(porta, baud_rate, timeout=1) as ser:
                if isinstance(comando, str):
                    comando = comando.encode()  # Garante que é bytes
                ser.write(comando)
                log.append(f"✅ Comando enviado (interno): {comando.decode().strip()}")
        except serial.SerialException as e:
            log.append(f"❌ Erro ao enviar comando para a porta serial: {str(e)}")
        except Exception as e:
            log.append(f"❌ Erro inesperado: {str(e)}")

    def exibir_resultado(self, raw_response, latencia, log):
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

            if response_str and "OK" in response_str.upper():
                st.success("🔍 Firewall validado e relay seguro.")
            elif response_str:
                st.warning(f"❗ Resposta inesperada: '{response_str}' — verifique o firmware.")
            else:
                st.error("❌ Nenhuma resposta válida foi interpretada.")

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

    def decodificar_resposta(self, raw, log):
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

    def exibir_analise_xor(self, raw_response):
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
            st.success(f"""
                🔑 **Melhor chave identificada:** `{melhor_linha['Key']}`  
                📌 **Palavras detectadas:** `{melhor_linha['Palavra-chave Detectada']}`  
                🧾 **Texto decodificado:** `{melhor_linha['Texto Decodificado']}`  
                💡 **Razão de caracteres imprimíveis:** `{melhor_linha['Printable Ratio']:.2f}`
            """)
            st.markdown("### 📊 Tabela Completa de Correspondências XOR")
            st.dataframe(df_xor.reset_index(drop=True))
        else:
            st.info("Nenhuma correspondência XOR significativa encontrada.")