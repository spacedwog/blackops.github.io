class AzimovFirewall:
    def __init__(self):
        self.trusted_users = set()
        self.integrity = True

    def detect_threat(self, packet):
        return "malware" in packet["content"] or packet["source"] in ["blacklist.com"]

    def obey_order(self, user, order):
        if order["type"] == "ALLOW":
            if self.detect_threat(order["packet"]):
                print(f"[ALERTA] Ordem rejeitada: ameaçaria segurança digital do usuário ({user})")
                return False  # Primeira Lei
        print(f"[INFO] Ordem do usuário {user} obedecida.")
        return True  # Segunda Lei

    def process_packet(self, packet):
        if self.detect_threat(packet):
            print(f"[BLOQUEIO] Ameaça detectada de {packet['source']}.")
            return False
        print(f"[PERMITIDO] Tráfego de {packet['source']} permitido.")
        return True

    def check_integrity(self):
        if not self.integrity:
            print("[ERRO] Integridade comprometida. Autorreparo ativado.")
            self.repair()
        else:
            print("[OK] Firewall íntegro.")

    def repair(self):
        print("[REPARO] Sistema de proteção restaurado.")
        self.integrity = True

    def apply_law_zero(self, threat_to_society):
        if threat_to_society:
            print("[AÇÃO GLOBAL] Desconectando sistema infectado para proteger a rede maior.")
            return True
        return False

# === Exemplo de uso ===
fw = AzimovFirewall()

# Tráfego legítimo
fw.process_packet({"source": "example.com", "content": "hello world"})

# Tráfego malicioso
fw.process_packet({"source": "blacklist.com", "content": "malware payload"})

# Ordem de liberar ameaça (violaria a Primeira Lei)
fw.obey_order("admin", {"type": "ALLOW", "packet": {"source": "blacklist.com", "content": "malware"}})

# Lei Zero em ação
fw.apply_law_zero(threat_to_society=True)

# Verificação de integridade
fw.check_integrity()