from aiogram import Router, types, F
from aiogram.filters import Command
import logging

from database.crud import Database
from openai_integration.client import OpenAIClient
from config import Config

# Создаем роутер
router = Router()

@router.callback_query(F.data == "consult")
async def consult(callback: types.CallbackQuery):
    logging.info(f"Пользователь {callback.from_user.id} запросил консультацию.")
    db = Database()
    await db.connect()

    # Получаем события пользователя
    events = await db.get_user_events(callback.from_user.id)
    await db.close()

    if not events:
        await callback.message.answer("У вас пока нет событий. Сначала создайте событие.")
        return

    # Формируем запрос для ChatGPT
    prompt = "У пользователя есть следующие события:\n\n"
    for event in events:
        event_date = event["event_date"].strftime("%Y-%m-%d %H:%M")
        prompt += f"- {event['event_name']} ({event_date})\n"
        if event["event_description"]:
            prompt += f"  Описание: {event['event_description']}\n"

    prompt += "\nДайте рекомендации по подготовке к этим событиям."

    # Запрашиваем ответ у ChatGPT
    openai_client = OpenAIClient()
    advice = await openai_client.get_advice(prompt)
    await callback.message.answer(advice)

# Функция для регистрации хэндлеров
def register_consult_handlers(dp):
    dp.include_router(router)