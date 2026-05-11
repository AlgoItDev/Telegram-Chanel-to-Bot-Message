from pyrogram import Client, filters
from config import API_ID, API_HASH, SESSION_NAME, SOURCE_CHANNEL_ID, TARGET_CHANNEL_ID
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
    """Poll the source channel for new messages and forward them."""
    while True:
        try:
            # Get the last processed message ID from the database
            last_id = database.get_last_message_id() or 0

            # Fetch recent messages from the source channel (newest first)
            # We limit to 20 to avoid too many requests, but adjust as needed
            messages = []
            async for message in app.get_chat_history(SOURCE_CHANNEL_ID, limit=20):
                messages.append(message)

            # Process messages in chronological order (oldest first)
            for message in reversed(messages):
                if message.id > last_id:
                    print(f"[INFO] Yeni mesaj: {message.id}")
                    await handlers.forward_message(client=app, message=message)
                    # Update last_id after each successful forward to avoid reprocessing if we crash
                    database.set_last_message_id(message.id)
                    # Small delay to avoid rate limits
                    await asyncio.sleep(0.5)

            # Wait before next poll
            await asyncio.sleep(5)  # Poll every 5 seconds

        except Exception as e:
            print(f"[ERROR] Polling hatasi: {e}")
            await asyncio.sleep(10)  # Wait longer on error


@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    await message.reply(
        "[INFO] Aktarici calisiyor (polling modu).\n\nKaynak: {}\nHedef: {}".format(
            SOURCE_CHANNEL_ID, TARGET_CHANNEL_ID
        )
    )


@app.on_message(filters.command("status") & filters.private)
async def status_command(client, message):
    last_id = database.get_last_message_id()
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
    print(LOGO, flush=True)
    print("[INFO] Bot baslatiliyor...", flush=True)
    print(f"[INFO] Kaynak: {SOURCE_CHANNEL_ID}", flush=True)
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
        app.stop()
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
