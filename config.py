import os
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

class Config:
    # Токен Telegram бота
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

    # Ключ API OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # URL базы данных PostgreSQL
    DATABASE_URL = os.getenv("DATABASE_URL")

    # Настройки планировщика
    SCHEDULER_TIMEZONE = "Europe/Moscow"

    # Другие настройки (если нужны)
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"