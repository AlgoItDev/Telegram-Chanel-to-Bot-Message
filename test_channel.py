from pyrogram import Client
from config import API_ID, API_HASH, SESSION_NAME, SOURCE_CHANNEL_ID
import asyncio

app = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH)

async def test():
    async with app:
        print(f"🔍 Kanal ID: {SOURCE_CHANNEL_ID}")
        try:
            chat = await app.get_chat(SOURCE_CHANNEL_ID)
            print(f"✅ Kanal bulundu: {chat.title}")
            print(f"   Type: {chat.type}")
            print(f"   ID: {chat.id}")
        except Exception as e:
            print(f"❌ Hata: {e}")

        print("\n📋 Tüm diyaloglar taranıyor...")
        async for dialog in app.get_dialogs():
            chat = dialog.chat
            if chat.type in ['channel', 'group', 'supergroup']:
                print(f"  - {chat.id} | {chat.type} | {chat.title}")

        print("\n📥 Son mesajlar alınıyor...")
        try:
            async for message in app.get_chat_history(SOURCE_CHANNEL_ID, limit=5):
                print(f"  Mesaj: {message.id} - {message.text or message.caption or '[medya]'}")
        except Exception as e:
            print(f"❌ Mesaj alma hatası: {e}")

asyncio.run(test())