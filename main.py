import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
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
async def on_startup(bot: Bot, base_url: str):
    await bot.set_webhook(f"{base_url}/webhook")
    logging.info(f"Вебхук установлен: {base_url}/webhook")

async def on_shutdown(bot: Bot):
    await bot.delete_webhook()
    logging.info("Вебхук удален.")

async def handle_root(request: web.Request):
    return web.Response(text="Bot is running!")

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

    # Настройка вебхука
    base_url = Config.WEBHOOK_URL  # URL вашего сервера

    # Используем замыкание для передачи base_url в on_startup
    async def on_startup_wrapper(bot: Bot):
        await on_startup(bot, base_url)

    dp.startup.register(on_startup_wrapper)
    dp.shutdown.register(on_shutdown)

    # Создание aiohttp приложения
    app = web.Application()
    app.router.add_get("/", handle_root)  # Добавляем обработчик для корневого пути
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_requests_handler.register(app, path="/webhook")
    setup_application(app, dp, bot=bot)

    # Запуск сервера
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=int(Config.PORT))
    await site.start()

    logging.info(f"Сервер запущен на {base_url}")
    await asyncio.Event().wait()  # Бесконечное ожидание
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Бот завершает работу...")
        print('_____________________________________EXIT_BOT______________________________________')
