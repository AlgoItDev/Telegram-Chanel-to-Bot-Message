from pyrogram import Client
from config import API_ID, API_HASH, SESSION_NAME, SOURCE_CHANNEL_ID, TARGET_CHANNEL_ID
import asyncio
import database

async def test():
    app = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH)
    async with app:
        print("[TEST] Connected")
        
        last_id = database.get_last_message_id()
        print(f"[TEST] Last ID: {last_id}")
        
        messages = []
        async for msg in app.get_chat_history(SOURCE_CHANNEL_ID, limit=5):
            messages.append(msg)
            print(f"[TEST] Message: {msg.id} - {msg.text or msg.caption or '[media]'}")
        
        print(f"[TEST] Total messages: {len(messages)}")
        
        if messages:
            newest = max(messages, key=lambda m: m.id)
            print(f"[TEST] Newest ID: {newest.id}")
            if not last_id or newest.id > last_id:
                print("[TEST] Yeni mesaj var!")

asyncio.run(test())