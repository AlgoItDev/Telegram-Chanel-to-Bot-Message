from pyrogram import filters
from config import SOURCE_CHANNEL_ID, TARGET_CHANNEL_ID, FILTER_KEYWORDS
import database

async def forward_message(client, message):
    try:
        if message.chat.id != SOURCE_CHANNEL_ID:
            return

        print(f"📩 Yeni mesaj: {message.id} - {(message.text or message.caption or '[medya]')[:50]}")

        last_id = database.get_last_message_id()
        if last_id and message.id <= last_id:
            print(f"  → Zaten işlendi, atlanıyor")
            return

        if FILTER_KEYWORDS:
            if not any(k.lower() in (message.text or "").lower() for k in FILTER_KEYWORDS):
                return

        text = ""
        if message.text:
            text = message.text
        elif message.caption:
            text = message.caption

        if message.photo:
            await client.send_photo(TARGET_CHANNEL_ID, message.photo.file_id, caption=text)
            print(f"  → Fotoğraf gönderildi")
        elif message.video:
            await client.send_video(TARGET_CHANNEL_ID, message.video.file_id, caption=text)
            print(f"  → Video gönderildi")
        elif message.document:
            await client.send_document(TARGET_CHANNEL_ID, message.document.file_id, caption=text)
            print(f"  → Dosya gönderildi")
        elif message.sticker:
            await client.send_sticker(TARGET_CHANNEL_ID, message.sticker.file_id)
            print(f"  → Sticker gönderildi")
        elif message.animation:
            await client.send_animation(TARGET_CHANNEL_ID, message.animation.file_id, caption=text)
            print(f"  → Animation gönderildi")
        else:
            if text:
                await client.send_message(TARGET_CHANNEL_ID, text)
                print(f"  → Mesaj gönderildi")

        database.set_last_message_id(message.id)

    except Exception as e:
        print(f"Hata: {e}")
        # Log to file for debugging
        with open("debug.log", "a", encoding="utf-8") as f:
            f.write(f"Hata: {e}\n")