from pyrogram import Client
from config import API_ID, API_HASH, SESSION_NAME
import asyncio

app = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH)

async def list_chats():
    async with app:
        me = await app.get_me()
        print(f"👤 Hesap: {me.first_name}\n")
        print("📋 Kanallar ve Gruplar:\n")

        async for dialog in app.get_dialogs():
            chat = dialog.chat
            if chat.type in ['channel', 'supergroup']:
                print(f"ID: {chat.id} | {chat.type} | {chat.title}")

asyncio.run(list_chats())