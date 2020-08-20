import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = str(os.getenv("BOT_TOKEN"))
FOOTBALL_API_KEY: str = str(os.getenv("FOOTBALL_API_TOKEN"))
DB_FILENAME: str = "data/sqllite/db/media.db"
WKHTMLTOIMAGE: str = str(os.getenv("WKHTMLTOIMAGE_PATH"))
TEMPLATES_DIR: str = "data/templates/"
ROW_SIZE: int = 6

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
