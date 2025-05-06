import os
import joblib
import streamlit as st
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Simula um firewall simples com autenticação de variáveis por chave
class Firewall:
    def __init__(self):
        self.autorizacoes = {}  # {'variavel_destino': 'chave_autorizada'}

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