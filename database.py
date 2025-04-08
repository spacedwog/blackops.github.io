import sqlite3

class Database:
    def __init__(self, db_name="users.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_table()

    def create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT,
                name TEXT,
                picture TEXT
            )
        """)
        self.conn.commit()

    def upsert_user(self, user):
        self.conn.execute("""
            INSERT INTO users (id, email, name, picture)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                email=excluded.email,
                name=excluded.name,
                picture=excluded.picture
        """, (user['id'], user['email'], user['name'], user['picture']))
        self.conn.commit()

    def get_user(self, user_id):
        cursor = self.conn.execute("SELECT * FROM users WHERE id=?", (user_id,))
        return cursor.fetchone()

db = Database()