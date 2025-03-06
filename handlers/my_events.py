# from aiogram import Router, types, F
# from aiogram.filters import Command
# import logging

# from database.crud import Database
# from config import Config

# # Создаем роутер
# router = Router()

# @router.message(Command("my_events"))
# @router.callback_query(F.data == "my_events")  # Обработчик для Inline-кнопки
# async def my_events(event: types.Message | types.CallbackQuery):
#     # Получаем объект message
#     if isinstance(event, types.CallbackQuery):
#         message = event.message
#     else:
#         message = event

#     logging.info(f"Пользователь {message.from_user.id} запросил свои события.")
#     db = Database()
#     await db.connect()

#     # Получаем события пользователя
#     events = await db.get_user_events(message.from_user.id)
#     await db.close()

#     if not events:
#         await message.answer("У вас пока нет событий.")
#         return

#     # Формируем сообщение со списком событий
#     events_list = "Ваши события:\n\n"
#     for event in events:
#         event_date = event["event_date"].strftime("%Y-%m-%d %H:%M")
#         events_list += f"📅 {event['event_name']}\n"
#         events_list += f"📝 {event['event_description']}\n" if event["event_description"] else ""
#         events_list += f"⏰ {event_date}\n\n"

#     await message.answer(events_list)

# # Функция для регистрации хэндлеров
# def register_my_events_handlers(dp):
#     dp.include_router(router)

from aiogram import Router, types, F
from aiogram.filters import Command
import logging

from database.crud import get_user_events  # Импортируем функцию
from keyboards.reply import create_reply_menu_keyboard
from config import Config

# Создаем роутер
router = Router()

@router.callback_query(F.data == "my_events")
async def my_events(callback_query: types.CallbackQuery):
    logging.info(f"Пользователь {callback_query.from_user.id} запросил свои события.")
    events = await get_user_events(callback_query.from_user.id)  # Используем функцию

    if not events:
        await callback_query.message.answer("У вас пока нет событий.")
        return

    # Формируем сообщение со списком событий
    events_list = "Ваши события:\n\n"
    for event in events:
        event_date = event["event_date"].strftime("%Y-%m-%d %H:%M")
        events_list += f"📅 {event['event_name']}\n"
        if event["event_description"]:  # Добавляем описание, если оно есть
            events_list += f"📝 {event['event_description']}\n"
        events_list += f"⏰ {event_date}\n\n"

    # Отправляем сообщение с событиями
    await callback_query.message.answer(events_list, reply_markup=create_reply_menu_keyboard())

    
# Функция для регистрации хэндлеров
def register_my_events_handlers(dp):
    dp.include_router(router)