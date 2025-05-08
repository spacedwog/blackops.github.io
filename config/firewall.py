import os
import joblib
import hashlib
import logging
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
        # Aqui você pode colocar regras reais de firewall
        regras_autorizadas = {
            "modelo_ia": True,
            "github_repo": recurso is not None and recurso.startswith("user/")  # ajuste o prefixo conforme seu uso
        }
        return regras_autorizadas.get(tipo, False)
        
    def transferir_via_firewall(self, modelo):  # sourcery skip: move-assign
        # Firewall para autenticação de variáveis
        chave_usuario = st.text_input("🔐 Chave de acesso (ex: secret123)")
        destino_nome = "modelo_autenticado"
        self.registrar_autorizacao(destino_nome, "secret123")  # chave válida predefinida

        variaveis_transmissao = {}

        if st.button("🚀 Transferir modelo via Firewall"):
            sucesso = self.transferir(modelo, destino_nome, variaveis_transmissao, chave_usuario)
            if sucesso:
                st.toast("✅ Modelo transferido com sucesso para variável protegida!")
            else:
                st.error("❌ Acesso negado! Chave incorreta ou sem permissão.")

            if destino_nome in variaveis_transmissao:
                st.write("🔎 Modelo disponível na variável protegida. Exemplo de predição:")
                pred = variaveis_transmissao[destino_nome].predict([[5.1, 3.5, 1.4, 0.2]])
                st.write(f"🔮 Predição: {pred}")

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