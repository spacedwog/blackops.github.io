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