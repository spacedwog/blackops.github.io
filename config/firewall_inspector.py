import subprocess
import streamlit as st
import platform
import re

class FirewallInspector:
    @staticmethod
    def verificar_firewall():  # sourcery skip: use-fstring-for-concatenation
        portas = {
            "HTTPS (443)": 443,
            "HTTP (80)": 80,
            "SSH (22)": 22
        }

        sistema = platform.system()
        st.write("**Sistema detectado:** " + sistema)
        st.write("**Regras do Firewall (tempo real):**")

        for servico, porta in portas.items():
            try:
                if sistema == "Windows":
                    comando = [
                        "netsh", "advfirewall", "firewall", "show", "rule", "name=all"
                    ]
                    resultado = subprocess.run(
                        comando,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        shell=True
                    )
                    if resultado.returncode != 0:
                        raise ValueError(resultado.stderr.strip())

                    regras = resultado.stdout or ""
                    
                    if not regras.strip():
                        raise ValueError("A saída do comando netsh está vazia.")

                    # Regex para encontrar se há regra permitindo a porta
                    padrao = r"(?i)port\s*:\s*" + str(porta) + r".*?action\s*:\s*allow"
                    permitido = bool(re.search(padrao, regras, re.DOTALL))

                    status = "✅ Permitido" if permitido else "⛔ Bloqueado"
                    st.write("• " + servico + ": " + status)

                else:
                    st.write("• " + servico + ": ⚠️ Sistema não suportado para verificação direta.")

            except Exception as e:
                st.error("Erro ao verificar " + servico + ": " + str(e))