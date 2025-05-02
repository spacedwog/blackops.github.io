import subprocess
import streamlit as st
import platform
import socket
import psutil
import ctypes

class FirewallInspector:
    WHOIS_SERVIDORES = {
        "com": "whois.verisign-grs.com",
        "net": "whois.verisign-grs.com",
        "org": "whois.pir.org",
        "br": "whois.registro.br",
        "io": "whois.nic.io",
        "xyz": "whois.nic.xyz",
        "info": "whois.afilias.net",
        "biz": "whois.biz",
        "dev": "whois.nic.google",
    }

    @staticmethod
    def detectar_whois_server(dominio):
        try:
            tld = dominio.strip().split(".")[-1].lower()
            return FirewallInspector.WHOIS_SERVIDORES.get(tld, "whois.iana.org")
        except Exception:
            return "whois.iana.org"

    @staticmethod
    def verificar_firewall_porta_43():
        comando = 'netsh advfirewall firewall show rule name=all | findstr /R /C:"43"'
        resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        return resultado.stdout.strip()

    @staticmethod
    def bloquear_porta_43_windows():
        if not FirewallInspector.is_admin():
            return "❌ Este comando requer privilégios de administrador! Execute o Streamlit como Administrador."

        comando = 'netsh advfirewall firewall add rule name="Bloquear Porta 43" dir=out action=block protocol=TCP remoteport=43'
        resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        return resultado.stdout or resultado.stderr

    @staticmethod
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except Exception:
            return False

    @staticmethod
    def listar_conexoes_43():
        # sourcery skip: inline-immediately-returned-variable
        conexoes = [conn for conn in psutil.net_connections() if conn.raddr and conn.raddr.port == 43]
        return conexoes

# === Streamlit App ===

# sourcery skip: use-fstring-for-concatenation, use-named-expression
st.title("🛡️ Proteção da Porta 43 (Windows)")
sistema = platform.system()
if sistema != "Windows":
    st.error("Este app foi projetado exclusivamente para Windows.")
    st.stop()

st.sidebar.header("Ações")

if st.sidebar.button("🔍 Verificar Regras de Firewall para Porta 43"):
    regras = FirewallInspector.verificar_firewall_porta_43()
    if regras:
        st.success("✅ Regras existentes para porta 43 detectadas:")
        st.code(regras)
    else:
        st.warning("⚠️ Nenhuma regra para porta 43 detectada. A porta pode estar aberta.")

if st.sidebar.button("⛔ Bloquear Porta 43 (Firewall)"):
    resultado = FirewallInspector.bloquear_porta_43_windows()
    if "requer privilégios" in resultado:
        st.error(resultado)
    else:
        st.success("✅ Comando executado:")
        st.code(resultado)

st.subheader("🔍 Conexões Ativas na Porta 43")
conexoes = FirewallInspector.listar_conexoes_43()
if conexoes:
    for conn in conexoes:
        st.write(" - " + str(conn.raddr.ip) + ":" + str(conn.raddr.port) + " | PID: " + str(conn.pid))
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