import subprocess
import streamlit as st
import platform
import socket
import psutil

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
    def verificar_firewall():  # sourcery skip: use-fstring-for-concatenation, use-named-expression
        sistema = platform.system()
        st.write("**Sistema detectado:**", sistema)

        st.subheader("🧱 Status da Porta 43 (WHOIS)")
        if sistema == "Windows":
            comando = 'netsh advfirewall firewall show rule name=all | findstr /R /C:"43"'
            resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
            if resultado.stdout.strip():
                st.success("✅ Porta 43 tem regras definidas (possivelmente permitida).")
            else:
                st.warning("⚠️ Nenhuma regra de firewall encontrada para a porta 43.")
        else:
            st.info("⚠️ Verificação de firewall só é suportada nativamente no Windows nesta versão.")

        st.subheader("🔍 Conexões ativas na porta 43")
        conexoes = [conn for conn in psutil.net_connections() if conn.raddr and conn.raddr.port == 43]
        if conexoes:
            for conn in conexoes:
                st.write("• " + conn.raddr.ip + ":" + str(conn.raddr.port) + " - PID: " + str(conn.pid))
        else:
            st.success("✅ Nenhuma conexão ativa detectada na porta 43.")

    @staticmethod
    def bloquear_porta_43():
        # sourcery skip: remove-unnecessary-else, swap-if-else-branches
        sistema = platform.system()
        if sistema == "Windows":
            comando = 'netsh advfirewall firewall add rule name="Bloquear Porta 43" dir=out action=block protocol=TCP remoteport=43'
            resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
            return resultado.stdout or resultado.stderr
        else:
            return "Bloqueio automático só disponível no Windows nesta versão."

# Streamlit App

# sourcery skip: use-fstring-for-concatenation, use-named-expression
st.title("🛡️ Proteção WHOIS e Porta 43")

st.sidebar.header("Ações")
if st.sidebar.button("🔍 Verificar Porta 43"):
    FirewallInspector.verificar_firewall()

if st.sidebar.button("⛔ Bloquear Porta 43 (Simulado)"):
    resultado = FirewallInspector.bloquear_porta_43()
    st.code(resultado)

st.sidebar.markdown("---")

st.subheader("📡 Consulta WHOIS")
dominio = st.text_input("Digite o domínio:", value="github.com")

if dominio:
    servidor_whois = FirewallInspector.detectar_whois_server(dominio)
    st.write("Servidor WHOIS:", servidor_whois)

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((servidor_whois, 43))
        s.send((dominio + "\r\n").encode())
        resposta = b""
        while True:
            dados = s.recv(4096)
            if not dados:
                break
            resposta += dados
        s.close()

        whois_texto = resposta.decode(errors="ignore")
        st.text_area("📄 Resultado WHOIS", whois_texto.strip(), height=300)
    except Exception as e:
        st.error("Erro na consulta WHOIS: " + str(e))