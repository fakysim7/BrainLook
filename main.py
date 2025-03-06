import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from config import Config
from handlers import register_handlers

# Настройка логирования
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,  # Уровень логирования (INFO, DEBUG, WARNING, ERROR, CRITICAL)
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Формат сообщений
        handlers=[
            logging.FileHandler("bot.log"),  # Логи в файл
            logging.StreamHandler(),  # Логи в консоль
        ],
    )
    logging.info("Логирование настроено.")

# Инициализация бота и диспетчера
async def main():
    setup_logging()  # Настройка логирования
    logging.info("Запуск бота...")

    # Используем DefaultBotProperties для передачи parse_mode
    bot = Bot(
        token=Config.TELEGRAM_BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())

    # Регистрация хэндлеров
    register_handlers(dp)

    # Запуск бота
    logging.info("Бот запущен и ожидает сообщений...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Бот завершает работу...")
        print('_____________________________________EXIT_BOT______________________________________')
