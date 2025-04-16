# -----------------------------
# auth/auditoria.py
# -----------------------------
import sqlite3
import datetime

class AuditoriaLogger:
    @staticmethod
    def registrar_atividade(usuario, acao, status, detalhes=""):
        """
        Registra uma entrada de auditoria na tabela `auditoria` do banco.
        """
        timestamp = datetime.datetime.now().isoformat()
        
        try:
            conn = sqlite3.connect("cloud_store.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO auditoria (usuario, acao, status, detalhes, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (usuario, acao, status, detalhes, timestamp))
            conn.commit()
        finally:
            conn.close()