# -----------------------------
# ui/streamlit_interface.py
# -----------------------------
import os
import time
import yaml
import subprocess
import streamlit as st
from ai.ocr_rfid import stream_camera
from typing import Any, Dict, Optional
from pymongo import MongoClient, errors
from core.github_utils import get_repo_info
from network.port_scanner import scan_ports
from core.mongo_viewer import MongoDBViewer
from core.relay_control import activate_relay
from core.sqlite_fallback import SQLiteFallback 
from ai.voice_control import VoiceGitHubAssistant
from network.firewall_checker import check_firewall_rules

class StreamlitInterface:
    def __init__(self, token: str, mongo_uri: str, repo_name: str):
        self.token = token
        self.mongo_uri = mongo_uri
        self.repo_name = repo_name
        self.mongo_operacional = self.check_mongo_connection()   # <-- adicionado
        self.firewall_ativo = False

    def check_mongo_connection(self) -> bool:
        """
        Testa a conexão com o MongoDB.
        """
        try:
            client = MongoClient(self.mongo_uri, serverSelectionTimeoutMS=3000)
            client.server_info()
            return True
        except errors.ServerSelectionTimeoutError:
            return False

    def load_config(self) -> Dict[str, Any]:
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'settings.yaml')
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)

    def show_comandos_disponiveis(self) -> None:
        st.markdown("---")
        st.markdown("### 🎙️ Comandos de Voz Disponíveis")
        comandos = [
            "Qual o último commit do projeto?",
            "Resuma o repositório OpenAI Whisper.",
            "Quantas issues estão abertas?",
            "Quais são as pull requests?",
            "Em qual linguagem esse repositório está programado?"
        ]
        for comando in comandos:
            st.markdown(f"- `{comando}`")

    def show_project_info(self) -> None:
        col_status, col_comandos = st.columns(2)

        with col_status:
            st.markdown("---")
            st.header("📡 Status do Repositório GitHub")

            repo_info = get_repo_info(self.repo_name, self.token)

            if "error" in repo_info:
                st.error(f"Erro ao buscar dados do GitHub: {repo_info['error']}")
            else:
                st.markdown(f"**🔗 Repositório:** `{repo_info['name']}`")
                st.markdown(f"**📝 Descrição:** {repo_info['description']}`")
                st.markdown(f"**📦 Linguagem Principal:** `{repo_info['language']}`")
                st.markdown(f"**⭐ Estrelas:** `{repo_info['stars']}`")
                st.markdown(f"**🐞 Issues Abertas:** `{repo_info['open_issues']}`")
                st.markdown(f"**🕒 Último Commit:** `{repo_info['last_commit']}`")

        with col_comandos:
            self.show_comandos_disponiveis()

        st.markdown("---")
        st.header("⚙️ Comandos de Controle")

        col1, col2, col3, col4, col5 = st.columns(5)
        funcao: Optional[str] = None

        with col1:
            if st.button("Ativar Relay 🔌"):
                funcao = 'activate_relay'
        with col2:
            if st.button("Scan de Portas 🌐"):
                funcao = 'scan_port'
        with col3:
            if st.button("Verificar Firewall 🔥"):
                self.firewall_ativo = not self.firewall_ativo
        with col4:
            if st.button("Comando de Voz 🎙️"):
                funcao = 'voice_command'
        with col5:
            if st.button("📡 Iniciar Live da Câmera"):
                funcao = 'stream_camera'

        self.executar_funcao(funcao)

        st.markdown("---")
        st.markdown("✅ Módulos Ativos:")
        st.markdown("- 🔌 Controle de Relay (GPIO)")
        st.markdown("- 🌐 Verificador de Firewall e Portas")
        st.markdown("- 🎙️ Reconhecimento de voz")
        st.markdown("- 📷 OCR e Transmissão de vídeo")
        st.markdown("- 🧠 Módulos de IA e Física")
        st.markdown("- 📊 Interface Streamlit")
        if self.mongo_operacional:
            st.markdown("- 🗄️ Mongo Database")
        else:
            st.markdown("- 🗄️ Backup Local com SQLite3")

        st.success("Sistema pronto para operação tática.")

    def executar_funcao(self, funcao: Optional[str]) -> None:
        placeholder = st.empty()

        if funcao == 'activate_relay':
            activate_relay()
            st.success("Relay ativado com sucesso!")
        elif funcao == 'scan_port':
            portas = scan_ports()
            st.code(f"Portas abertas: {portas}")
        elif funcao == 'verify_firewall':
            self.firewall_ativo = not self.firewall_ativo
        elif funcao == 'voice_command':
            assistant = VoiceGitHubAssistant(self.token, self.mongo_uri, self.repo_name)
            resultado = assistant.executar_voz()
            st.write(resultado)
        elif funcao == 'stream_camera':
            stream_camera()

        if self.firewall_ativo:
            status = check_firewall_rules()
            with placeholder.container():
                st.subheader("📡 Status Atual do Firewall")
                for rule in status:
                    st.markdown(f"- {rule}")
            time.sleep(3)

    def show_mongo_viewer(self) -> None:

        if st.button("🔄 Abrir Gráfico DNS"):
            try:
                comando = "./executar_graficodns.ps1"
                resultado = subprocess.run(
                    ["powershell", "-Command", comando],
                    capture_output=True,
                    text=True,
                    shell=True
                )
                st.code(resultado.stdout or resultado.stderr)
            except Exception as e:
                st.error(f"Erro ao executar: {e}")
        """
        Exibe o visualizador de dados.
        Usa MongoDB se disponível; caso contrário, usa SQLite3 como fallback.
        """
        if self.mongo_operacional:
            mongodb_viewer = MongoDBViewer(self.mongo_uri)
            mongodb_viewer.view_collection("nome_do_banco", "nome_da_colecao")
            mongodb_viewer.exibir_mongodb()
        else:
            st.warning("⚠️ MongoDB indisponível. Usando Backup Local com SQLite3.")
            sqlite_fallback = SQLiteFallback()
            sqlite_fallback.display_data()