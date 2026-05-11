import aiosqlite
import os

DB_FILE = "data.db"

async def init_db():
    os.makedirs(os.path.dirname(DB_FILE) if os.path.dirname(DB_FILE) else ".", exist_ok=True)
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS state
                     (key TEXT PRIMARY KEY, value TEXT)''')
        await db.commit()

async def get_last_message_id():
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute("SELECT value FROM state WHERE key = 'last_message_id'") as cursor:
            result = await cursor.fetchone()
            return int(result[0]) if result else None

async def set_last_message_id(msg_id):
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute("INSERT OR REPLACE INTO state (key, value) VALUES ('last_message_id', ?)", (str(msg_id),))
        await db.commit()

# Initialize on first use - will be called from main.py before any DB operation