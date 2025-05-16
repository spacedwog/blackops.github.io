# -----------------------------
# framework/firewall.py
# -----------------------------
import json
from typing import List, Dict

class FirewallRule:
    def __init__(self, source_ip, dest_ip, port, action):
        self.source_ip = source_ip
        self.dest_ip = dest_ip
        self.port = port
        self.action = action  # "allow" ou "deny"

    def to_dict(self):
        return {
            "source_ip": self.source_ip,
            "dest_ip": self.dest_ip,
            "port": self.port,
            "action": self.action
        }

class Firewall:
    def __init__(self, rules_file='rules.json'):
        self.rules_file = rules_file
        self.rules = self.load_rules()
        
    def add_whois_rules(self, source_ip, dest_ip, port, action):
        rule = FirewallRule(source_ip=source_ip, dest_ip=dest_ip, port=port, action=action)
        self.add_rule(rule)

    def load_rules(self) -> List[FirewallRule]:
        try:
            with open(self.rules_file, 'r') as f:
                data = json.load(f)
                return [FirewallRule(**rule) for rule in data]
        except FileNotFoundError:
            return []

    def save_rules(self):
        with open(self.rules_file, 'w') as f:
            json.dump([r.to_dict() for r in self.rules], f, indent=4)

    def add_rule(self, rule: FirewallRule):
        self.rules.append(rule)
        self.save_rules()

    def remove_rule(self, index: int):
        if 0 <= index < len(self.rules):
            del self.rules[index]
            self.save_rules()
            
    def clear_rules(self):
        self.rules = []
        self.save_rules()

    def check_packet(self, source_ip, dest_ip, port) -> str:
        return next(
            (
                rule.action
                for rule in self.rules
                if rule.source_ip in [source_ip, '*']
                and rule.dest_ip in [dest_ip, '*']
                and (str(rule.port) == str(port) or rule.port == '*')
            ),
            "allow",
        )