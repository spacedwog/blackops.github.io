# -----------------------------
# core/sqlite_fallback.py
# -----------------------------
import sqlite3
import streamlit as st

class SQLiteFallback:
    def __init__(self, db_path="local_backup.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS backup_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT
            )
        ''')
        self.conn.commit()

    def insert_data(self, data: str):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO backup_data (data) VALUES (?)', (data,))
        self.conn.commit()

    def fetch_all(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM backup_data')
        return cursor.fetchall()

    def display_data(self):
        st.subheader("📄 Visualização de Dados (SQLite3)")
        rows = self.fetch_all()
        for row in rows:
            st.markdown(f"- **ID:** {row[0]} | **Dados:** {row[1]}")