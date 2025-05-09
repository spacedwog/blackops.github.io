import psutil
import socket
import platform
import subprocess
import streamlit as st

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
        # Adicione mais TLDs conforme necessário
    }

    @staticmethod
    def detectar_whois_server(dominio):
        try:
            tld = dominio.strip().split(".")[-1].lower()
            return FirewallInspector.WHOIS_SERVIDORES.get(tld, "whois.nic.br")
        except Exception:
            return "whois.nic.br"

    @staticmethod
    def verificar_firewall():
        portas = {
            "HTTPS (443)": "443",
            "WHOIS (43)": "43",
            "HTTP (80)": "80",
            "SSH (22)": "22"
        }

        sistema = platform.system()
        st.write("**Sistema detectado:**", sistema)
        st.write("**Regras do Firewall (tempo real):**")

        for servico, porta in portas.items():
            try:
                if sistema == "Windows":
                    comando = f'netsh advfirewall firewall show rule name=all | findstr /R /C:"{porta}"'
                    resultado = subprocess.run(
                        comando,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        shell=True
                    )
                    saida = resultado.stdout or ""
                    if saida.strip():
                        status = "✅ Permitido (detectado uso da porta)"
                    else:
                        status = "⛔ Bloqueado ou não configurado (sem regra visível)"
                    st.write(f"• {servico}: {status}")
                else:
                    st.write(f"• {servico}: ⚠️ Sistema não suportado para verificação direta.")
            except Exception as e:
                st.error(f"Erro ao verificar {servico}: {str(e)}")

        # 🔍 Consulta WHOIS com detecção de servidor
        st.write("---")
        st.subheader("🔎 Consulta WHOIS (porta 43)")
        dominio = st.text_input("Digite o domínio para consulta WHOIS:", value="github.com")

        if dominio:
            servidor_whois = FirewallInspector.detectar_whois_server(dominio)
            st.write(f"**Servidor WHOIS detectado:** {servidor_whois}")

            if FirewallInspector.porta_bloqueada(servidor_whois):
                st.error(f"🚫 A conexão à porta 43 no servidor '{servidor_whois}' está bloqueada. Verifique seu firewall ou permissões de rede.")
            else:
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
                    if whois_texto.strip():
                        st.text_area(f"📄 WHOIS de {dominio}", whois_texto.strip(), height=300)
                    else:
                        st.warning("⚠️ Resposta WHOIS vazia.")
                except Exception as e:
                    st.error(f"Erro inesperado na consulta WHOIS ({servidor_whois}): {str(e)}")

        # 🔘 Teste manual da porta 43
        st.write("---")
        st.subheader("🧪 Teste Manual da Porta 43 (WHOIS)")

        servidor_teste = st.text_input("Servidor WHOIS para teste manual (ex: whois.verisign-grs.com)", value="whois.verisign-grs.com")
        if st.button("🔌 Testar conexão WHOIS"):
            if FirewallInspector.porta_bloqueada(servidor_teste):
                st.error(f"🚫 Porta 43 bloqueada ou sem permissão para se conectar a {servidor_teste}.")
            else:
                st.success(f"✅ Porta 43 acessível em {servidor_teste}. Conexão permitida.")

    @staticmethod
    def porta_bloqueada(servidor):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((servidor, 43))
            s.close()
            return False
        except PermissionError:
            return True
        except Exception:
            return False

    @staticmethod
    def bloquear_porta():
        sistema = platform.system()
        if sistema != "Windows":
            return "Bloqueio automático só disponível no Windows nesta versão."
        comando = 'netsh advfirewall firewall add rule name="Bloquear Porta 43" dir=out action=block protocol=TCP remoteport=43'
        resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        return resultado.stdout or resultado.stderr

    @staticmethod
    def listar_conexoes():
        return [
            conn
            for conn in psutil.net_connections()
            if conn.raddr and conn.raddr.port == 43
        ]