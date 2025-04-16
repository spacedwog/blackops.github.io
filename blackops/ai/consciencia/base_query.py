# --------------------------------------
# consciencia/base_query.py
# --------------------------------------
import sys
from pprint import pprint
from pymongo import MongoClient

# Função para garantir que o texto seja impresso sem erros de codificação
def safe_print(text):
    sys.stdout.buffer.write((text + "\n").encode('utf-8', errors='replace'))

class VoiceGitHubAssistantQuery:
    def __init__(self, mongo_uri, database_name):
        self.mongo_uri = mongo_uri
        self.database_name = database_name
        self.client = None
        self.db = None

    def conectar(self):
        try:
            self.client = MongoClient(self.mongo_uri)
            self.db = self.client[self.database_name]
            safe_print("✅ Conectado ao MongoDB com sucesso.")
        except Exception as e:
            safe_print(f"❌ Erro na conexão com MongoDB: {e}")

    def buscar_por_comando_normalizado(self, comando, colecao):
        if self.db is None:
            safe_print("⚠️ Banco de dados não está conectado.")
            return []

        try:
            filtro = {"comando_normalizado": comando}
            resultados = self.db[colecao].find(filtro)
            return list(resultados)
        except Exception as e:
            safe_print(f"❌ Erro ao buscar documentos: {e}")
            return []

    def desconectar(self):
        if self.client:
            self.client.close()
            safe_print("🔌 Conexão com MongoDB encerrada.")

    def exibir_resultados(self, documentos):
        safe_print(f"📊 Resultados para comando_normalizado = 'estatísticas de voz':\n")
        for doc in documentos:
            pprint(doc)