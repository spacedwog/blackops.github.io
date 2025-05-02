import subprocess
import streamlit as st
import platform
import socket
import psutil
import ctypes
from firewall_inspector import FirewallInspector

st.title("🛡️ Proteção da Porta(Windows)")
sistema = platform.system()
if sistema != "Windows":
    st.error("Este app foi projetado exclusivamente para Windows.")
    st.stop()

st.sidebar.header("Ações")

if st.sidebar.button("🔍 Verificar Regras de Firewall para Porta 43"):
    regras = FirewallInspector.verificar_firewall()
    if regras:
        st.success("✅ Regras existentes para porta 43 detectadas:")
        st.code(regras)
    else:
        st.warning("⚠️ Nenhuma regra para porta 43 detectada. A porta pode estar aberta.")

if st.sidebar.button("⛔ Bloquear Porta 43 (Firewall)"):
    resultado = FirewallInspector.bloquear_porta()
    if "requer privilegios" in resultado:
        st.error(resultado)
    else:
        st.success("✅ Comando executado:")
        st.code(resultado)

st.subheader("🔍 Conexões Ativas na Porta 43")
conexoes = FirewallInspector.listar_conexoes()
if conexoes:
    for conn in conexoes:
        st.write("- " + str(conn.raddr.ip) + ":" + str(conn.raddr.port) + " | PID: " + str(conn.pid))
else:
    st.success("✅ Nenhuma conexão ativa na porta 43.")

st.subheader("🔎 Consulta WHOIS (porta 43)")
dominio = st.text_input("Digite o domínio:", value="github.com")

if dominio:
    servidor = FirewallInspector.detectar_whois_server(dominio)
    st.write("Servidor WHOIS:", servidor)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((servidor, 43))
        s.send((dominio + "\r\n").encode())
        resposta = b""
        while True:
            dados = s.recv(4096)
            if not dados:
                break
            resposta += dados
        s.close()
        texto = resposta.decode(errors="ignore")
        st.text_area("📄 Resposta WHOIS", texto.strip(), height=300)
    except Exception as e:
        st.error("Erro na consulta: " + str(e))