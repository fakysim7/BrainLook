from aiogram import Router, types
from aiogram.filters import Command
import logging

from database.crud import Database

# Создаем роутер
router = Router()

@router.message(Command("check_db"))
async def check_db(message: types.Message):
    logging.info(f"Пользователь {message.from_user.id} запросил проверку базы данных.")
    db = Database()
    if await db.connect():
        if await db.check_connection():
            await message.answer("Подключение к базе данных успешно установлено.")
        else:
            await message.answer("Ошибка при проверке подключения к базе данных.")
        await db.close()
    else:
        await message.answer("Не удалось подключиться к базе данных.")

# Функция для регистрации хэндлеров
def register_check_db_handlers(dp):
    dp.include_router(router)