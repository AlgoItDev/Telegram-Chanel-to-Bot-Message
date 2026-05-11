from pyrogram import filters
from pyrogram.errors import FloodWait
from config import SOURCE_CHANNEL_IDS, TARGET_CHANNEL_ID, FILTER_KEYWORDS
import database
import asyncio

async def forward_message(client, message):
    try:
        if message.chat.id not in SOURCE_CHANNEL_IDS:
            return

        print(f"[INFO] Yeni mesaj: {message.id}")

        # Get text from message or caption
        text = message.text or message.caption or ""

        # Filter keywords - check both text and caption
        if FILTER_KEYWORDS:
            if not any(k.lower() in text.lower() for k in FILTER_KEYWORDS):
                print(f"  -> Filtre disi, atlanıyor")
                return

        # Media group (album) handling
        if message.media_group_id:
            print(f"  -> Album mesaji, atlanıyor (album destegi eklenebilir)")
            return

        # Send message with flood wait handling
        async def send_with_retry(func, *args, **kwargs):
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    await func(*args, **kwargs)
                    return True
                except FloodWait as e:
                    print(f"  -> FloodWait: {e.value} saniye bekleniyor...")
                    await asyncio.sleep(e.value)
                    if attempt == max_retries - 1:
                        raise
            return False

        if message.photo:
            await send_with_retry(client.send_photo, TARGET_CHANNEL_ID, message.photo.file_id, caption=text)
            print(f"  -> Fotoğraf gönderildi")
        elif message.video:
            await send_with_retry(client.send_video, TARGET_CHANNEL_ID, message.video.file_id, caption=text)
            print(f"  -> Video gönderildi")
        elif message.document:
            await send_with_retry(client.send_document, TARGET_CHANNEL_ID, message.document.file_id, caption=text)
            print(f"  -> Dosya gönderildi")
        elif message.sticker:
            await send_with_retry(client.send_sticker, TARGET_CHANNEL_ID, message.sticker.file_id)
            print(f"  -> Sticker gönderildi")
        elif message.animation:
            await send_with_retry(client.send_animation, TARGET_CHANNEL_ID, message.animation.file_id, caption=text)
            print(f"  -> Animation gönderildi")
        else:
            if text:
                await send_with_retry(client.send_message, TARGET_CHANNEL_ID, text)
                print(f"  -> Mesaj gönderildi")

        await database.set_last_message_id(message.id)

    except Exception as e:
        print(f"[ERROR] Hata: {e}")