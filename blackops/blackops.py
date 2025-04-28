# -----------------------------
# blackops/blackops.py
# -----------------------------

import os
import sqlite3
import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
from security.monitor import CyberSecurityMonitor
from ai.voice_control import VoiceGitHubAssistant
from ui.streamlit_interface import StreamlitInterface
from security.firebase_connector import FirebaseConnector

# Configurações
DB_PATH = "blackops_data.db"  # Banco de dados local
TABLE_NAME = "comandos"       # Nome da tabela

def main():
    st.markdown("### ⚫ BLACKOPS IA")
    aba1, aba2, aba3, aba4 = st.tabs([
        "🧬 Blackops (Sistema Nervoso)",
        "🧠 Blackops (Cérebro)",
        "🧫 Blackops (Interface)",
        "🤖 Blackops (Consciência Virtual)"
    ])

    mongo_uri = "mongodb+srv://twitchcombopunch:6z2h1j3k9F.@clusterops.iodjyeg.mongodb.net/"
    token = os.getenv("GITHUB_TOKEN")
    repo_name = "openai/whisper"

    streamlit_interface = StreamlitInterface(token=token, mongo_uri=mongo_uri, repo_name=repo_name)

    with aba1:
        streamlit_interface.show_project_info()

    with aba2:
        streamlit_interface.show_mongo_viewer()

    with aba3:
        st.markdown("### 🧫 BLACKOPS MONITOR")
        try:
            aba_monitoramento, aba_ameacas, aba_mitigacao, aba_cybertela = st.tabs([
                "🔍 Monitoramento",
                "🛡️ Ameaças",
                "🧱 Mitigação",
                "⚔️ CyberTela"
            ])
            with aba_monitoramento:
                CyberSecurityMonitor.exibir_monitoramento()
            with aba_ameacas:
                CyberSecurityMonitor.exibir_lista_ameacas()
            with aba_mitigacao:
                CyberSecurityMonitor.executar_resposta_mitigacao_completa()
            with aba_cybertela:
                CyberSecurityMonitor.exibir_visual_cyberpunk()
        except Exception as e:
            st.error(f"Erro ao carregar o monitoramento: {e}")

    with aba4:
        st.info("🔍 Buscando comandos com 'estatísticas de voz'...")

        resultados = buscar_comandos_firebase("estatísticas de voz")

        if resultados:
            exibir_estatisticas_de_voz(resultados, token, repo_name)
            resultados_filtrados = filtrar_por_repositorio(resultados)
            exibir_linha_do_tempo(resultados_filtrados)
            buscar_por_palavra_chave(resultados_filtrados)
            exibir_comandos_em_tabela(resultados_filtrados)
            exibir_mapa_de_calor(resultados_filtrados)
            exportar_para_csv(resultados_filtrados)
        else:
            st.warning("Nenhum comando encontrado.")

# -----------------------------
# Funções Auxiliares
# -----------------------------

def buscar_comandos_firebase(comando_normalizado):
    try:
        firebase = FirebaseConnector(credentials_path="blackops/security/firebase_key.json")
        return firebase.buscar_comandos(comando_normalizado)
    except Exception as e:
        st.error(f"Erro ao acessar Firebase: {e}")
        return []

def exibir_estatisticas_de_voz(resultados, github_token=None, repo_name=None):
    total = len(resultados)
    acertos = sum(1 for r in resultados if "acertou" in r.get("resposta", "").lower())
    erros = sum(1 for r in resultados if "erro" in r.get("resposta", "").lower() or "não entendi" in r.get("resposta", "").lower())
    precisao = (acertos / total * 100) if total else 0

    st.subheader("📊 Estatísticas Gerais")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total", total)
    col2.metric("Acertos", acertos)
    col3.metric("Erros", erros)
    col4.metric("Precisão (%)", f"{precisao:.2f}")

    assistente = VoiceGitHubAssistant(github_token=github_token, mongo_uri=None, repo_name=repo_name)
    assistente.speak(f"Você efetuou {total} comandos, acertou {acertos} e errou {erros} com precisão de {precisao:.2f}%.")
    assistente.interagir_por_voz()

def filtrar_por_repositorio(resultados):
    repos = sorted({r.get("repo", "desconhecido") for r in resultados})
    filtro = st.selectbox("📁 Filtrar por repositório:", repos)
    return [r for r in resultados if r.get("repo") == filtro]

def exibir_linha_do_tempo(resultados):
    st.subheader("🕓 Linha do Tempo dos Comandos")

    data = [{
        "Timestamp": r.get("timestamp"),
        "Comando": r.get("comando_original"),
        "Resposta": r.get("resposta")
    } for r in resultados]

    df = pd.DataFrame(data)
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    df = df.sort_values("Timestamp")

    st.line_chart(df.set_index("Timestamp").assign(Comandos=1).resample("1min").count())

def buscar_por_palavra_chave(resultados):
    termo = st.text_input("🔍 Buscar por palavra-chave:")
    if termo:
        filtrados = [r for r in resultados if termo.lower() in r.get("comando_original", "").lower()]
        exibir_comandos_em_tabela(filtrados)

def exibir_comandos_em_tabela(resultados):
    st.subheader("📋 Comandos Registrados")
    for r in resultados:
        with st.expander(f"🧠 {r.get('comando_original', 'Sem comando')}"):
            st.write("🔁 Normalizado:", r.get("comando_normalizado"))
            st.write("📎 Repositório:", r.get("repo"))
            st.write("🕒 Timestamp:", r.get("timestamp"))
            st.success(r.get("resposta", "Sem resposta"))

def exibir_mapa_de_calor(resultados):
    st.subheader("🌡️ Mapa de Calor por Horário")

    df = pd.DataFrame([{
        "hora": pd.Timestamp(r["timestamp"]).hour,
        "dia": pd.Timestamp(r["timestamp"]).day_name()
    } for r in resultados])

    pivot = df.groupby(["dia", "hora"]).size().unstack(fill_value=0)
    dias_ordenados = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    pivot = pivot.reindex(dias_ordenados)

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.heatmap(pivot, ax=ax, cmap="YlGnBu", cbar_kws={'label': 'Qtd Comandos'})
    st.pyplot(fig)

def exportar_para_csv(resultados):
    if st.button("📤 Exportar para CSV"):
        df = pd.DataFrame(resultados)
        st.download_button("⬇️ Download", df.to_csv(index=False), file_name="comandos_blackops.csv", mime="text/csv")

# Execução principal
if __name__ == "__main__":
    main()