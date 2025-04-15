# -----------------------------
# ui/streamlit_interface.py
# -----------------------------
import os
import yaml
import streamlit as st
from typing import Any, Dict, Optional
from ai.ocr_rfid import stream_camera
from core.github_utils import get_repo_info
from network.port_scanner import scan_ports
from core.relay_control import activate_relay
from streamlit_autorefresh import st_autorefresh
from ai.voice_control import activate_voice_control
from network.firewall_checker import check_firewall_rules


def load_config() -> Dict[str, Any]:
    """
    Carrega o arquivo de configuração YAML.

    Returns:
        Load: Configurações carregadas do arquivo YAML.
    """
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'settings.yaml')
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


def show_comandos_disponiveis() -> None:
    """
    Exibe a lista de comandos de voz disponíveis na interface Streamlit.

    Returns:
        Show (None): Configurações carregadas do arquivo YAML.
    """
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


def show_project_info() -> None:
    """
    Exibe informações do repositório GitHub, comandos e ações interativas na interface Streamlit.

    Returns:
        Project (None): Configurações carregadas do arquivo YAML.
    """
    config = load_config()
    st_autorefresh(interval=60000, key="github_auto_refresh")

    st.markdown("---")
    st.header("📡 Status do Repositório GitHub")

    token = os.getenv("8928341d3b422e184b621364a45885f6a2baa804")
    repo_name = "openai/whisper"

    repo_info = get_repo_info(repo_name, token)

    if "error" in repo_info:
        st.error(f"Erro ao buscar dados do GitHub: {repo_info['error']}")
    else:
        st.markdown(f"**🔗 Repositório:** `{repo_info['name']}`")
        st.markdown(f"**📝 Descrição:** {repo_info['description']}`")
        st.markdown(f"**📦 Linguagem Principal:** `{repo_info['language']}`")
        st.markdown(f"**⭐ Estrelas:** `{repo_info['stars']}`")
        st.markdown(f"**🐞 Issues Abertas:** `{repo_info['open_issues']}`")
        st.markdown(f"**🕒 Último Commit:** `{repo_info['last_commit']}`")

    show_comandos_disponiveis()

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
            funcao = 'verify_firewall'
    with col4:
        if st.button("Comando de Voz 🎙️"):
            funcao = 'voice_command'
    with col5:
        if st.button("📡 Iniciar Live da Câmera"):
            funcao = 'stream_camera'

    executar_funcao(funcao)

    st.markdown("---")
    st.markdown("✅ Módulos Ativos:")
    st.markdown("- 🔌 Controle de Relay (GPIO)")
    st.markdown("- 🌐 Verificador de Firewall e Portas")
    st.markdown("- 🎙️ Reconhecimento de voz")
    st.markdown("- 📷 OCR e Transmissão de vídeo")
    st.markdown("- 🧠 Módulos de IA e Física")
    st.markdown("- 📊 Interface Streamlit")

    st.success("Sistema pronto para operação tática.")


def executar_funcao(funcao: Optional[str]) -> None:
    """
    Executa a função associada a um botão da interface Streamlit.

    Returns:
        Funcao (Optional[str]): Nome da função a ser executada.
    """
    if funcao == 'activate_relay':
        activate_relay()
        st.success("Relay ativado com sucesso!")
    elif funcao == 'scan_port':
        portas = scan_ports()
        st.code(f"Portas abertas: {portas}")
    elif funcao == 'verify_firewall':
        regras = check_firewall_rules()
        st.code("\n".join(regras))
    elif funcao == 'voice_command':
        resultado = activate_voice_control()
        st.success(resultado)
        st.info(resultado)
    elif funcao == 'stream_camera':
        stream_camera()