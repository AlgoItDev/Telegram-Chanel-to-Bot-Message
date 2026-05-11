import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
SESSION_NAME = os.getenv("SESSION_NAME", "my_session")

SOURCE_CHANNEL_ID = int(os.getenv("SOURCE_CHANNEL_ID", 0))
TARGET_CHANNEL_ID = int(os.getenv("TARGET_CHANNEL_ID", 0))

FILTER_KEYWORDS = os.getenv("FILTER_KEYWORDS", "").split(",")
FILTER_KEYWORDS = [k.strip() for k in FILTER_KEYWORDS if k.strip()]