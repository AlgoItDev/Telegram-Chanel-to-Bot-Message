import sqlite3
import os

DB_FILE = "data.db"

def init_db():
    os.makedirs(os.path.dirname(DB_FILE) if os.path.dirname(DB_FILE) else ".", exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS state
                 (key TEXT PRIMARY KEY, value TEXT)''')
    conn.commit()
    conn.close()

def get_last_message_id():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT value FROM state WHERE key = 'last_message_id'")
    result = c.fetchone()
    conn.close()
    return int(result[0]) if result else None

def set_last_message_id(msg_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO state (key, value) VALUES ('last_message_id', ?)", (str(msg_id),))
    conn.commit()
    conn.close()

init_db()