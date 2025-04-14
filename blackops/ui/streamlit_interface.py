# -----------------------------
# ui/streamlit_interface.py
# -----------------------------
import os
import yaml
import streamlit as st
from ai.ocr_rfid import stream_camera
from network.port_scanner import scan_ports
from core.relay_control import activate_relay
from ai.voice_control import activate_voice_control
from network.firewall_checker import check_firewall_rules

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'settings.yaml')
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def show_project_info():
    config = load_config()

    st.set_page_config(page_title=config['app_name'], layout="centered")

    st.title(f"🔒 {config['app_name']} v{config['version']}")
    st.subheader("📡 Interface de Cibersegurança Ativa")

    st.markdown(f"**Autor:** `{config['author']}`")
    st.markdown("### 📝 Descrição")
    st.info(config['description'])

    st.markdown("---")
    st.markdown("✅ Módulos Ativos:")
    st.markdown("- 🔌 Controle de Relay (GPIO)")
    st.markdown("- 🌐 Verificador de Firewall e Portas")
    st.markdown("- 🎙️ Reconhecimento de voz")
    st.markdown("- 📷 OCR e Transmissão de vídeo")
    st.markdown("- 🧠 Módulos de IA e Física")
    st.markdown("- 📊 Interface Streamlit")

    st.markdown("---")
    st.header("⚙️ Comandos de Controle")

    col1, col2, col3, col4, col5 = st.columns(5)

    funcao = None

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

    st.success("Sistema pronto para operação tática.")

def executar_funcao(funcao):

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
        st.info(resultado)
    elif funcao == 'stream_camera':
        stream_camera()
        