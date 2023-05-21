from dotenv import load_dotenv
import os


load_dotenv()

CHANNEL_ACCESS_TOKEN = os.getenv('CHANNEL_ACCESS_TOKEN')
CHANNEL_SECRET = os.getenv('CHANNEL_SECRET')
HANK_ID = os.getenv('HANK_ID')
LALA_ID = os.getenv('LALA_ID')
MONGO_URL = os.getenv('MONGO_URL')