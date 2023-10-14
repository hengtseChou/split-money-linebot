import os

from dotenv import load_dotenv

if not load_dotenv():
    raise Exception(".env file not found.")

CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")
HANK_ID = os.getenv("HANK_ID")
LALA_ID = os.getenv("LALA_ID")
MONGO_URL = os.getenv("MONGO_URL")
ENV = os.getenv("ENV")
