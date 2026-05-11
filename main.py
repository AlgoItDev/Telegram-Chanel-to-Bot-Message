from pyrogram import Client, filters
from config import API_ID, API_HASH, SESSION_NAME, SOURCE_CHANNEL_IDS, TARGET_CHANNEL_ID
import handlers
import database
import asyncio
import sys

# Ensure UTF-8 encoding for stdout on Windows
if sys.platform == "win32":
    import io

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

app = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH)


async def poll_for_new_messages():
    """Poll the source channels for new messages and forward them."""
    while True:
        try:
            # Get the last processed message ID from the database
            last_id = await database.get_last_message_id() or 0

            # Poll each source channel
            for channel_id in SOURCE_CHANNEL_IDS:
                try:
                    messages = []
                    async for message in app.get_chat_history(channel_id, limit=20):
                        messages.append(message)

                    # Process messages in chronological order (oldest first)
                    for message in reversed(messages):
                        if message.id > last_id:
                            print(f"[INFO] Yeni mesaj: {message.id}")
                            await handlers.forward_message(client=app, message=message)
                            await database.set_last_message_id(message.id)
                            await asyncio.sleep(0.5)

                except Exception as e:
                    print(f"[ERROR] Kanal {channel_id} hatasi: {e}")

            # Wait before next poll
            await asyncio.sleep(5)

        except Exception as e:
            print(f"[ERROR] Polling genel hatasi: {e}")
            await asyncio.sleep(10)


@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    await message.reply(
        f"[INFO] Aktarici calisiyor (polling modu).\n\nKaynak: {SOURCE_CHANNEL_IDS}\nHedef: {TARGET_CHANNEL_ID}"
    )


@app.on_message(filters.command("status") & filters.private)
async def status_command(client, message):
    last_id = await database.get_last_message_id()
    await message.reply(f"[INFO] Durum\n\nSon islenen mesaj ID: {last_id}")


LOGO = """
   █████████   █████         █████████     ███████   
  ███░░░░░███ ░░███         ███░░░░░███  ███░░░░░███ 
 ░███    ░███  ░███        ███     ░░░  ███     ░░███
 ░███████████  ░███       ░███         ░███      ░███
 ░███░░░░░███  ░███       ░███    █████░███      ░███
 ░███    ░███  ░███      █░░███  ░░███ ░░███     ███ 
 █████   █████ ███████████ ░░█████████  ░░░███████░  
░░░░░   ░░░░░ ░░░░░░░░░░░   ░░░░░░░░░     ░░░░░░░                                                    
          ALGO IT TELEGRAM FORWARDER
"""


async def main():
    # Initialize database
    await database.init_db()

    print(LOGO, flush=True)
    print("[INFO] Bot baslatiliyor...", flush=True)
    print(f"[INFO] Kaynak: {SOURCE_CHANNEL_IDS}", flush=True)
    print(f"[INFO] Hedef: {TARGET_CHANNEL_ID}", flush=True)
    print("[INFO] Baglaniyor...", flush=True)
    sys.stdout.flush()

    await app.start()
    print("[SUCCESS] Bot baglandi!", flush=True)

    # Start the polling task
    polling_task = asyncio.create_task(poll_for_new_messages())

    # Keep the bot running until interrupted
    while True:
        try:
            await asyncio.sleep(3600)  # Sleep for 1 hour (allows Ctrl+C to work)
        except (KeyboardInterrupt, asyncio.CancelledError):
            print("\n[INFO] Bot durduruluyor...", flush=True)
            break

    # Cleanup
    polling_task.cancel()
    try:
        await asyncio.wait_for(polling_task, timeout=2.0)
    except:
        pass

    try:
        await app.stop()
    except:
        pass

    print("[INFO] Bot durdu", flush=True)


if __name__ == "__main__":
    # Windows için UTF-8 ayarı
    import os

    os.environ["PYTHONIOENCODING"] = "utf-8"
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("[INFO] Bot durduruldu")
    except SystemExit:
        pass
