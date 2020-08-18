import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
FOOTBALL_API_KEY = str(os.getenv("FOOTBALL_API_TOKEN"))
DB_FILENAME = "data/sqllite/db/media.db"
WKHTMLTOIMAGE = str(os.getenv("WKHTMLTOIMAGE_PATH"))
TEMPLATES_DIR = "data/templates/"

admins = [
    296320278
]

ip = os.getenv("ip")

aiogram_redis = {
    'host': ip,
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}
