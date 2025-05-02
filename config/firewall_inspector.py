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
            return FirewallInspector.WHOIS_SERVIDORES.get(tld, "whois.iana.org")
        except Exception:
            return "whois.iana.org"

    @staticmethod
    def verificar_firewall():
        # sourcery skip: use-fstring-for-concatenation, use-named-expression
        portas = {
            "HTTPS (443)": "443",
            "HTTP (80)": "80",
            "SSH (22)": "22"
        }

        sistema = platform.system()
        st.write("**Sistema detectado:**", sistema)
        st.write("**Regras do Firewall (tempo real):**")

        for servico, porta in portas.items():
            try:
                if sistema == "Windows":
                    comando = 'netsh advfirewall firewall show rule name=all | findstr /R /C:"' + porta + '"'
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
                    st.write("• " + servico + ": " + status)
                else:
                    st.write("• " + servico + ": ⚠️ Sistema não suportado para verificação direta.")
            except Exception as e:
                st.error("Erro ao verificar " + servico + ": " + str(e))

        # 🔍 Consulta WHOIS com detecção de servidor
        st.write("---")
        st.subheader("🔎 Consulta WHOIS (porta 43)")
        dominio = st.text_input("Digite o domínio para consulta WHOIS:", value="github.com")

        if dominio:
            servidor_whois = FirewallInspector.detectar_whois_server(dominio)
            st.write("**Servidor WHOIS detectado:** " + servidor_whois)

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
                    st.text_area("📄 WHOIS de " + dominio, whois_texto.strip(), height=300)
                else:
                    st.warning("⚠️ Resposta WHOIS vazia.")
            except Exception as e:
                st.error("Erro na consulta WHOIS (" + servidor_whois + "): " + str(e))
                
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
        # sourcery skip: remove-unnecessary-else, swap-if-else-branches
        sistema = platform.system()
        if sistema == "Windows":
            comando = 'netsh advfirewall firewall add rule name="Bloquear Porta 43" dir=out action=block protocol=TCP remoteport=43'
            resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
            return resultado.stdout or resultado.stderr
        else:
            return "Bloqueio automático só disponível no Windows nesta versão."

    @staticmethod
    def listar_conexoes():  # sourcery skip: inline-immediately-returned-variable
        conexoes = [conn for conn in psutil.net_connections() if conn.raddr and conn.raddr.port == 43]
        return conexoes