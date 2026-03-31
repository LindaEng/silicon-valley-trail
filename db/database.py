import sqlite3

def get_connection(db_name="game.db"):
    return sqlite3.connect(db_name)

def init_db(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS saves (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            state TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()