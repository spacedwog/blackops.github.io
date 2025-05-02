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
    def verificar_firewall():
        comando = 'netsh advfirewall firewall show rule name=all | findstr /R /C:"43"'
        resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        return resultado.stdout.strip()

    @staticmethod
    def bloquear_porta():
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
    def listar_conexoes():
        return [conn for conn in psutil.net_connections() if conn.raddr and conn.raddr.port == 43]