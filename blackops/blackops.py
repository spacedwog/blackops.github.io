# -----------------------------
# blackops/blackops.py
# -----------------------------

import os
import json
import sqlite3
import requests 
import pandas as pd
import seaborn as sns
import streamlit as st
from threading import Thread
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify
from security.monitor import CyberSecurityMonitor
from ai.voice_control import VoiceGitHubAssistant
from ui.streamlit_interface import StreamlitInterface

# Inicializando Flask
app = Flask(__name__)

# Função para iniciar o Flask em um thread separado
def run_flask():
    app.run(host="0.0.0.0", port=5000)

# Configurações
DB_PATH = "blackops_data.db"  # Banco de dados local
TABLE_NAME = "comandos"       # Nome da tabela
API_ENDPOINT = "http://localhost:5000/receive_json"  # URL do endpoint para receber os dados

# Função para enviar dados via POST
def send_json_post(data):
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(API_ENDPOINT, json=data, headers=headers)
        if response.status_code == 200:
            st.success("Dados enviados com sucesso!")
        else:
            st.error(f"Erro ao enviar dados: {response.status_code}")
            st.json(response.json())
    except requests.exceptions.RequestException as e:
        st.error(f"Erro de conexão: {e}")

# Rota API para receber dados JSON
@app.route("/receive_json", methods=["POST"])
def receive_json():
    try:
        data = request.get_json()
        st.write(f"Dados recebidos: {data}")
        # Aqui você pode processar os dados conforme necessário
        return jsonify({"status": "success", "message": "Dados recebidos com sucesso!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

# Função para gerar a resposta de status
def get_status():
    response = {
                "status": "ok",
                "message": "BlackOps server is running!"
                }
    return json.dumps(response)

def main():
    st.markdown("### ⚫ BLACKOPS IA")
    aba1, aba2, aba3, aba4 = st.tabs([
        "🧬 Blackops (Sistema Nervoso)",
        "🧠 Blackops (Cérebro)",
        "🧫 Blackops (Interface)",
        "🤖 Blackops (Consciência Virtual)"
    ])

    mongo_uri = "mongodb+srv://twitchcombopunch:6z2h1j3k9F.@clusterops.iodjyeg.mongodb.net/"
    token = os.getenv("8928341d3b422e184b621364a45885f6a2baa804")
    repo_name = "openai/whisper"

    streamlit_interface = StreamlitInterface(token=token, mongo_uri=mongo_uri, repo_name=repo_name)

    with aba1:
        if st.button("🔄 Atualizar Status"):
            response = get_status()
            st.text(response)
        else:
            st.info("Clique no botão para atualizar o status.")

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

        resultados = buscar_comandos_localmente("estatísticas de voz")

        if resultados:
            exibir_estatisticas_de_voz(resultados, token, repo_name)
            resultados_filtrados = filtrar_por_repositorio(resultados)
            exibir_linha_do_tempo(resultados_filtrados)
            buscar_por_palavra_chave(resultados_filtrados)
            exibir_comandos_em_tabela(resultados_filtrados)
            exibir_mapa_de_calor(resultados_filtrados)
            exportar_para_csv(resultados_filtrados)

            # Enviar os dados filtrados para um endpoint externo via POST
            if st.button("📤 Enviar Dados para API"):
                send_json_post(resultados_filtrados)
        else:
            st.warning("Nenhum comando encontrado.")

# -----------------------------
# Funções Auxiliares
# -----------------------------

def buscar_comandos_localmente(comando_normalizado):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                comando_original TEXT,
                comando_normalizado TEXT,
                resposta TEXT,
                repo TEXT,
                timestamp TEXT
            )
        """)
        conn.commit()

        query = f"""
            SELECT comando_original, comando_normalizado, resposta, repo, timestamp
            FROM {TABLE_NAME}
            WHERE comando_normalizado LIKE ?
        """
        cursor.execute(query, (f"%{comando_normalizado}%",))
        rows = cursor.fetchall()

        colunas = ["comando_original", "comando_normalizado", "resposta", "repo", "timestamp"]
        resultados = [dict(zip(colunas, row)) for row in rows]

        return resultados
    except Exception as e:
        st.error(f"Erro ao acessar banco de dados local: {e}")
        return []
    finally:
        conn.close()

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
    # Rodar o Flask em um thread separado para não bloquear o Streamlit
    Thread(target=run_flask).start()
    main()