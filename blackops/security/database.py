# -----------------------------
# security/database.py
# -----------------------------
import sqlite3
from datetime import datetime
from pymongo import MongoClient, errors

class MongoDBHandler:
    def __init__(self):
        mongo_uri_remoto = "mongodb+srv://twitchcombopunch:6z2h1j3k9F.@clusterops.iodjyeg.mongodb.net/"
        self.use_mongo = True  # Flag para indicar se o MongoDB está sendo usado
        self.sqlite_db_path = 'blackops_local.db'

        try:
            self.client = MongoClient(mongo_uri_remoto, serverSelectionTimeoutMS=5000)
            self.client.server_info()  # Força conexão para validar
            print("[MongoDB] Conectado ao MongoDB Atlas com sucesso.")
            self.db_type = 'mongo'
            self.db = self.client['blackops']  # Nome do banco no MongoDB
            self.registros = self.db['registros']  # Coleção para registros normais
            self.ameacas = self.db['ameacas_detectadas']  # Coleção para ameaças detectadas
        except (errors.ServerSelectionTimeoutError, errors.ConfigurationError) as e:
            print(f"[MongoDB] Erro de conexão remota: {e}")
            print("[MongoDB] Usando fallback para SQLite3 local...")

            self.use_mongo = False
            self.db_type = 'sqlite'
            self.conn = sqlite3.connect(self.sqlite_db_path)
            self.cursor = self.conn.cursor()
            self._setup_sqlite()

    def _setup_sqlite(self):
        """Cria a estrutura básica do SQLite, se não existir."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS registros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT,
                info TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ameacas_detectadas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip TEXT,
                risco TEXT,
                detalhes TEXT,
                timestamp TEXT
            )
        ''')
        self.conn.commit()
        print("[SQLite3] Banco de dados local configurado.")

    def insert_data(self, data, info):
        """Insere dados genéricos (registros)."""
        if self.use_mongo:
            self.registros.insert_one({'data': data, 'info': info})
            print("[MongoDB] Registro inserido.")
        else:
            self.cursor.execute('INSERT INTO registros (data, info) VALUES (?, ?)', (data, info))
            self.conn.commit()
            print("[SQLite3] Registro inserido.")

    def find_data(self):
        """Busca registros genéricos."""
        if self.use_mongo:
            return list(self.registros.find())
        else:
            self.cursor.execute('SELECT * FROM registros')
            return self.cursor.fetchall()

    def registrar_ameaca(self, ip, risco, detalhes=None):
        """Registra uma nova ameaça."""
        registro = {
            "ip": ip,
            "risco": risco,
            "detalhes": detalhes or "Não especificado",
            "timestamp": datetime.now().isoformat()
        }

        if self.use_mongo:
            self.ameacas.insert_one(registro)
            print(f"[MongoDB] Ameaça registrada: {registro}")
        else:
            self.cursor.execute('''
                INSERT INTO ameacas_detectadas (ip, risco, detalhes, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (registro["ip"], registro["risco"], registro["detalhes"], registro["timestamp"]))
            self.conn.commit()
            print(f"[SQLite3] Ameaça registrada: {registro}")

    def listar_ameacas(self):
        """Lista as ameaças registradas."""
        if self.use_mongo:
            ameacas = list(self.ameacas.find().sort("timestamp", -1))
            print("[MongoDB] Ameaças listadas.")
            return ameacas
        else:
            self.cursor.execute('''
                SELECT ip, risco, detalhes, timestamp
                FROM ameacas_detectadas
                ORDER BY timestamp DESC
            ''')
            resultados = self.cursor.fetchall()
            ameacas = [{"ip": r[0], "risco": r[1], "detalhes": r[2], "timestamp": r[3]} for r in resultados]
            print("[SQLite3] Ameaças listadas.")
            return ameacas

    def apagar_todas(self):
        """Apaga todas as ameaças registradas."""
        if self.use_mongo:
            self.ameacas.delete_many({})
            print("[MongoDB] Todas as ameaças apagadas.")
        else:
            self.cursor.execute('DELETE FROM ameacas_detectadas')
            self.conn.commit()
            print("[SQLite3] Todas as ameaças apagadas.")