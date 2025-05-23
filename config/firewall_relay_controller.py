import time
import socket
import platform
import subprocess

class FirewallRelayController:
    def __init__(self, arduino_host="192.168.15.8", arduino_port=8080, test_host="whois.iana.org", firewall_port=43, timeout=3):
        self.test_host = test_host
        self.firewall_port = firewall_port
        self.timeout = timeout
        self.system = platform.system()
        self.arduino_host = arduino_host
        self.arduino_port = arduino_port
        self.response = self.send_arduino_command("GET /STATUS HTTP/1.1")

    def send_arduino_command(self, command):
        try:
            with socket.create_connection((self.arduino_host, self.arduino_port), timeout=self.timeout) as sock:
                sock.sendall((command + "\n").encode())
                time.sleep(1)
                response = sock.recv(1024).decode().strip()
                return response
        except Exception as e:
            return f"❌ Erro na comunicação com o Arduino: {e}"

    def check_port_access(self):
        try:
            with socket.create_connection((self.test_host, self.firewall_port), timeout=self.timeout):
                return True
        except (socket.timeout, ConnectionRefusedError, OSError):
            return False

    def check_firewall_rules(self):
        try:
            if self.system == "Linux":
                iptables_result = subprocess.run(
                    ["sudo", "iptables", "-L", "-n"],
                    capture_output=True, text=True
                )
                ufw_result = subprocess.run(
                    ["sudo", "ufw", "status", "numbered"],
                    capture_output=True, text=True
                )
                rules = iptables_result.stdout + ufw_result.stdout
                return f"dpt:{self.firewall_port}" in rules or f"{self.firewall_port}" in rules
            elif self.system == "Windows":
                netsh_result = subprocess.run(
                    ["netsh", "advfirewall", "firewall", "show", "rule", "name=all"],
                    capture_output=True, text=True, shell=True
                )
                return f"Port: {self.firewall_port}" in netsh_result.stdout
        except Exception as e:
            print(f"[!] Erro ao verificar regras de firewall: {e}")
        return False

    def list_possible_reasons(self):
        reasons = [
            "✔️ Política de segurança da rede exige bloqueio de portas não utilizadas.",
            "✔️ Configuração manual do administrador para bloquear tráfego na porta 43.",
            "✔️ Software antivírus/firewall de terceiros bloqueando portas por padrão.",
            "✔️ Presença de regras 'deny' em firewalls configurados pelo usuário.",
            "✔️ Firewall do roteador/modem ou gateway de rede bloqueando conexões WHOIS.",
        ]
        if self.system == "Linux":
            reasons.append("✔️ Regras ativas em iptables ou firewalld bloqueando a porta.")
            reasons.append("✔️ 'ufw' configurado para negar conexões de saída ou entrada na porta 43.")
        elif self.system == "Windows":
            reasons.append("✔️ Regras criadas com 'netsh' para bloquear tráfego de rede nessa porta.")
            reasons.append("✔️ Perfis de firewall (público/privado/domínio) desativando conexões WHOIS.")
        return reasons

    def get_firewall_status_and_control_relay(self):
        access = self.check_port_access()
        rule_block = self.check_firewall_rules()
        status = f"🔍 Verificando porta {self.firewall_port}...\n"

        if rule_block:
            status += f"⚠️ Regras de firewall detectadas para a porta {self.firewall_port}.\n"
        else:
            status += f"✅ Nenhuma regra explícita bloqueando a porta {self.firewall_port} encontrada.\n"

        if access:
            status += f"🟢 Porta {self.firewall_port} está acessível.\n"
        else:
            status += f"🔴 Porta {self.firewall_port} está inacessível. Firewall ou rede pode estar bloqueando.\n"

        return status

    def get_relay_status(self):
        """Envia STATUS e obtém o estado atual do relé."""
        if self.response.startswith("STATE:"):
            return "🟢 O relé está ligado." if self.response[6:] == "ON" else "🔴 O relé está desligado."
        elif self.response.startswith("LED:"):
            return "🟢 O LED está ligado." if self.response[4:] == "ON" else "🔴 O LED está desligado."
        elif self.response.startswith("[JAVA]"):
            mensagem = f"🟢 Conexão com JAVA estabelecida.<br>♨️ {self.response}"
            return mensagem
        else:
            return f"⚠️ Resposta inesperada: {self.response}"

    def diagnose_common_block_reasons(self):
        reasons = [
            "🔒 Firewall local (Windows Defender, iptables, ufw) pode estar bloqueando conexões WHOIS.",
            "🧱 Firewall de rede (roteador/modem) configurado para bloquear portas de saída incomuns.",
            "🏢 Políticas de segurança em redes corporativas bloqueiam portas que não sejam HTTP/HTTPS.",
            "🌐 ISP (provedor de internet) pode filtrar conexões WHOIS para evitar abusos automatizados.",
            "❌ O servidor WHOIS pode estar fora do ar ou recusar conexões do seu IP.",
            "🔧 Permissões do sistema operacional insuficientes para abrir sockets (Linux exige sudo em alguns casos).",
            "📦 Softwares antivírus/firewall de terceiros (ex: Kaspersky, McAfee) podem bloquear por padrão.",
        ]
        if self.system == "Linux":
            reasons += [
                "⚙️ Regras do iptables ou firewalld ativas bloqueando a porta 43.",
                "🛡️ UFW (Uncomplicated Firewall) configurado para negar conexões de saída nessa porta."
            ]
        elif self.system == "Windows":
            reasons += [
                "⚙️ Regras do Windows Firewall via netsh para bloquear tráfego na porta 43.",
                "🛡️ O perfil de rede (Público/Privado) do Windows pode bloquear conexões WHOIS."
            ]
        return reasons

    def detect_active_block_reasons(self):
        try:
            netsh_check = subprocess.run(
                ["netsh", "advfirewall", "firewall", "show", "rule", "name=all"],
                capture_output=True,
                text=True,
                check=True,
                shell=True  # Importante para Windows
            )
            output = netsh_check.stdout or ""
            if f"Port: {self.firewall_port}" in output:
                return f"🔴 A porta {self.firewall_port} está bloqueada."
            else:
                return f"🟢 A porta {self.firewall_port} está liberada."
        except subprocess.CalledProcessError as e:
            return f"Erro ao verificar regras de firewall: {e}"
        except Exception as e:
            return f"Erro inesperado ao verificar regras de firewall: {e}"

    def fetch_java_server_route(self, route="/STATUS"):
        """Consulta a rota HTTP simulada do servidor Java via socket TCP."""
        try:
            with socket.create_connection((self.arduino_host, self.arduino_port), timeout=self.timeout) as sock:
                request = f"GET {route} HTTP/1.1\r\nHost: {self.arduino_host}\r\n\r\n"
                sock.sendall(request.encode())
                time.sleep(0.5)
                response = sock.recv(4096).decode()
                return response.strip()
        except Exception as e:
            return f"❌ Erro ao requisitar {route}: {e}"

    # Métodos prontos para acessar as rotas específicas do servidor Java
    def get_status(self):
        return self.fetch_java_server_route("/STATUS")

    def get_blocked_reasons(self):
        return self.fetch_java_server_route("/BLOCKED")

    def run_diagnose(self):
        return self.fetch_java_server_route("/DIAGNOSE")

    def get_cyberbrain_status(self):
        return self.fetch_java_server_route("/CYBERBRAIN")

    def get_export_status(self):
        return self.fetch_java_server_route("/EXPORT")