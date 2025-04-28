import os
import firebase_admin
from firebase_admin import credentials, firestore

class FirebaseConnector:
    def __init__(self, credentials_path=None):
        if not firebase_admin._apps:
            cred = credentials.Certificate(credentials_path)
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def buscar_comandos(self, comando_normalizado):
        comandos_ref = self.db.collection("comandos")
        query = comandos_ref.where("comando_normalizado", ">=", comando_normalizado).where("comando_normalizado", "<=", comando_normalizado + "\uf8ff")
        docs = query.stream()
        return [doc.to_dict() for doc in docs]

    def adicionar_comando(self, comando_data):
        self.db.collection("comandos").add(comando_data)