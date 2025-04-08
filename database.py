# database.py
import sqlite3

conn = sqlite3.connect("cloud_store.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id TEXT PRIMARY KEY,
    email TEXT,
    nome TEXT,
    foto TEXT
)
""")
conn.commit()

def create_or_update_user(user):
    cursor.execute("""
        INSERT OR REPLACE INTO usuarios (id, email, nome, foto)
        VALUES (?, ?, ?, ?)
    """, (user["id"], user["email"], user["name"], user["picture"]))
    conn.commit()

def get_user(user_id):
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (user_id,))
    return cursor.fetchone()