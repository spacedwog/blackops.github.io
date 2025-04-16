# -----------------------------
# network/firewall_checker.py
# -----------------------------
import random
import time

firewall_templates = [
    ["Firewall ativo", "Regra: Bloqueio de porta 23", "Regra: Permitir HTTP/HTTPS"],
    ["Firewall ativo", "Regra: Bloqueio de IP malicioso", "Regra: Permitir tráfego interno"],
    ["Firewall inativo", "Todas as portas liberadas"],
    ["Firewall ativo", "Regra: IDS ativado", "Regra: Bloqueio automático de ataques DoS"]
]

def check_firewall_rules():
    """Retorna uma simulação dinâmica das regras do firewall."""
    return random.choice(firewall_templates)

def stream_firewall_status(interval=2):
    """Gera atualizações periódicas do firewall."""
    while True:
        yield check_firewall_rules()
        time.sleep(interval)
