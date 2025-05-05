import time
import socket
import serial
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
            self.relay_serial.write(b"OFF\n")  # Desliga o relé
        else:
            status += f"🔴 Porta {self.firewall_port} está inacessível. Firewall ou rede pode estar bloqueando.\n"
            self.relay_serial.write(b"ON\n")   # Liga o relé

        return status

# Exemplo de uso
if __name__ == "__main__":
    controller = FirewallRelayController(port="COM3")  # Ajuste conforme necessário
    print(controller.get_firewall_status_and_control_relay())
    print("\n📋 Motivos possíveis:")
    for reason in controller.list_possible_reasons():
        print("-", reason)