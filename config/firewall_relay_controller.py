import time
import socket
import serial
import logging
import platform
import subprocess

class FirewallRelayController:
    def __init__(self, port="COM3", baudrate=9600, test_host="whois.iana.org", firewall_port=43, timeout=3):
        self.test_host = test_host
        self.firewall_port = firewall_port
        self.timeout = timeout
        self.system = platform.system()
        self.relay_serial = serial.Serial(port, baudrate, timeout=2)
        time.sleep(2)  # Espera Arduino iniciar

    def check_port_access(self):  # sourcery skip: remove-redundant-exception
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
                if f"dpt:{self.firewall_port}" in rules or f"{self.firewall_port}" in rules:
                    return True
            elif self.system == "Windows":
                netsh_result = subprocess.run(
                    ["netsh", "advfirewall", "firewall", "show", "rule", "name=all"],
                    capture_output=True, text=True, shell=True
                )
                if f"Port: {self.firewall_port}" in netsh_result.stdout or f"{self.firewall_port}" in netsh_result.stdout:
                    return True
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
        try:
            self.relay_serial.reset_input_buffer()
            self.relay_serial.write(b"STATUS\n")
            time.sleep(1)  # Dá tempo para o Arduino responder
            response = self.relay_serial.readline().decode().strip()
            if response.startswith("STATE:"):
                if response[6:] == "ON":
                    return "🟢 O relé está ligado."
                elif response[6:] == "OFF":
                    return "🔴 O relé está desligado."
            elif response.startswith("LED:"):
                if response[4:] == "ON":
                    return "🟢 O LED está ligado."
                elif response[4:] == "OFF":
                    return "🔴 O LED está desligado."
            else:
                return f"⚠️ Resposta inesperada: {response}"
        except Exception as e:
            return f"❌ Erro ao obter estado do relé: {e}"
        
    def diagnose_common_block_reasons(self):
        """Retorna uma análise formatada dos motivos mais comuns para bloqueio da porta 43."""
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
    
    def detect_active_block_reasons(self):  # sourcery skip: extract-method
        """
        Executa um comando 'netsh' para verificar regras de firewall ativas
        e retorna se a porta especificada está bloqueada.
        """
        try:
            # Executa o comando netsh e captura a saída
            netsh_check = subprocess.run(
                ["netsh", "advfirewall", "firewall", "show", "rule", "name=all"],
                capture_output=True,
                text=True,
                check=True  # Gera exceção se o comando falhar
            )

            # Depuração: registrar a saída
            logging.debug("Comando netsh retornou código %s", netsh_check.returncode)
            logging.debug("STDOUT:\n%s", netsh_check.stdout)
            logging.debug("STDERR:\n%s", netsh_check.stderr)

            # Verifica se há um bloqueio para a porta
            if netsh_check.stdout and f"Port: {self.firewall_port}" in netsh_check.stdout:
                logging.info(f"Porta {self.firewall_port} bloqueada pelo firewall.")
                return f"A porta {self.firewall_port} está bloqueada."

            logging.info(f"Porta {self.firewall_port} não encontrada na lista de bloqueios.")
            return f"A porta {self.firewall_port} está liberada."

        except subprocess.CalledProcessError as e:
            logging.error("Erro ao executar netsh: %s", str(e))
            return "Erro ao verificar regras de firewall."

        except Exception as e:
            logging.error("Erro inesperado: %s", str(e))
            return "Erro inesperado ao verificar regras de firewall."

# Exemplo de uso
if __name__ == "__main__":
    controller = FirewallRelayController(port="COM3")  # Ajuste conforme necessário
    print(controller.get_firewall_status_and_control_relay())
    print("\n📋 Motivos possíveis:")
    for reason in controller.list_possible_reasons():
        print("-", reason)
    print("\n📋 Diagnóstico dos motivos mais prováveis para o bloqueio da porta 43:")
    for reason in controller.diagnose_common_block_reasons():
        print("-", reason)
    logging.basicConfig(level=logging.DEBUG)  # Ativa logs de depuração
    firewall = FirewallRelayController(firewall_port=43)  # Exemplo de porta
    resultado = firewall.detect_active_block_reasons()
    print(resultado)

