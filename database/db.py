# database/db.py

import sqlite3
from datetime import datetime

class UsuarioDB:
    def __init__(self, db_name="cloud_store.db"):
        self.db_name = db_name
        self.criar_tabela_usuarios()
        self.criar_tabela_rfid()
        self.criar_tabela_auditoria()

    def conectar(self):
        return sqlite3.connect(self.db_name)

    def criar_tabela_usuarios(self):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY,
                    login TEXT UNIQUE,
                    nome TEXT,
                    email TEXT,
                    avatar_url TEXT,
                    data_login TEXT
                )
            """)
            conn.commit()

    def criar_tabela_rfid(self):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS rfid_users (
                    uid TEXT PRIMARY KEY,
                    nome TEXT,
                    login_github TEXT,
                    nivel_acesso TEXT,
                    ultimo_acesso DATETIME
                );
            """)
            conn.commit()   

    def criar_tabela_auditoria(self):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS auditoria (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT,
                    acao TEXT,
                    status TEXT,
                    detalhes TEXT,
                    timestamp DATETIME
                );
            """)
            conn.commit()

    def salvar_usuario(self, user_data):
        with self.conectar() as conn:
            cursor = conn.cursor()

            now = datetime.now().isoformat()
            login = user_data.get("login")
            nome = user_data.get("name") or login
            email = user_data.get("email")
            avatar_url = user_data.get("avatar_url")

            cursor.execute("""
                INSERT OR REPLACE INTO usuarios (login, nome, email, avatar_url, data_login)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(login) DO UPDATE SET
                    nome=excluded.nome,
                    email=excluded.email,
                    avatar_url=excluded.avatar_url,
                    data_login=excluded.data_login
            """, (login, nome, email, avatar_url, now))

            conn.commit()

    def registrar_cartao(self, uid, nome, login_github, nivel_acesso):
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO rfid_users (uid, nome, login_github, nivel_acesso, ultimo_acesso)
                VALUES (?, ?, ?, ?, ?)
            """, (uid, nome, login_github, nivel_acesso, agora))
            conn.commit()

    def get_usuario_por_uid(self, uid):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM rfid_users WHERE uid = ?", (uid,))
            return cursor.fetchone()
