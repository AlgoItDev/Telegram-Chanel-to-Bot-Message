import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
SESSION_NAME = os.getenv("SESSION_NAME", "my_session")

# Support multiple source channels (comma separated)
SOURCE_CHANNEL_IDS_STR = os.getenv("SOURCE_CHANNEL_ID", "0")
SOURCE_CHANNEL_IDS = [int(x.strip()) for x in SOURCE_CHANNEL_IDS_STR.split(",") if x.strip()]
TARGET_CHANNEL_ID = int(os.getenv("TARGET_CHANNEL_ID", 0))

FILTER_KEYWORDS = os.getenv("FILTER_KEYWORDS", "").split(",")
FILTER_KEYWORDS = [k.strip() for k in FILTER_KEYWORDS if k.strip()]