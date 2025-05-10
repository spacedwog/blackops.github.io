import os
import json
import hashlib
from datetime import datetime
# Simula um firewall simples com autenticação de variáveis por chave
class Firewall:
    def __init__(self):
        self.autorizacoes = {}  # {'variavel_destino': 'chave_autorizada'}
        self.log_path = "./logs/firewall_transferencias.log"
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

    def registrar_autorizacao(self, var_destino, chave):
        self.autorizacoes[var_destino] = chave

    def autenticar(self, var_destino, chave):
        return self.autorizacoes.get(var_destino) == chave

    def transferir(self, origem, destino_nome, destino_dict, chave):
        if self.autenticar(destino_nome, chave):
            destino_dict[destino_nome] = origem
            return True
        else:
            return False

    def autorizar_transferencia(self, tipo, recurso=None):
        """
            Verifica se a transferência é autorizada com base no tipo e no recurso.
        """
        regras_autorizadas = {
            "modelo_ia": True,
            "github_info": recurso is not None,  # Permite exportação de dados GitHub autenticado
            "github_repo": recurso is not None and isinstance(recurso, str) and recurso.startswith("spacedwog/blackops.github.io")
        }

        # Criar um pacote compatível com a AzimovFirewall
        pacote = {
            "content": json.dumps(regras_autorizadas),
            "source": tipo
        }

        return regras_autorizadas.get(tipo, False)

        
    def transferir_via_firewall(self, dados, caminho="./dados_github", nome_arquivo="dados.json"):
        os.makedirs(caminho, exist_ok=True)
        destino = os.path.join(caminho, nome_arquivo)

        with open(destino, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

        integridade = self.calcular_hash(destino)
        self.registrar_log(f"TRANSFERÊNCIA AUTORIZADA: Dados GitHub exportados para {destino} | HASH: {integridade}")
        return destino

    def registrar_transferencia(self, tipo, recurso=None):
        data = datetime.now().isoformat()
        self.registrar_log(f"TRANSFERÊNCIA: tipo={tipo}, recurso={recurso}, data={data}")

    def calcular_hash(self, arquivo):
        sha256 = hashlib.sha256()
        with open(arquivo, "rb") as f:
            for bloco in iter(lambda: f.read(4096), b""):
                sha256.update(bloco)

        return sha256.hexdigest()

    def registrar_log(self, mensagem):

        with open(self.log_path, "a") as log:
            log.write(f"[{datetime.now().isoformat()}] {mensagem}\n")