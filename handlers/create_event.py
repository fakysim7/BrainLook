from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta
import logging

from keyboards.calendar import create_year_keyboard, create_month_keyboard, create_day_keyboard
from keyboards.time import create_time_keyboard
from keyboards.reply import create_reply_menu_keyboard
from database.crud import add_event  # Импортируем функцию
from scheduler.notifications import schedule_notification
from utils.states import EventState
from handlers.start import return_to_menu

# Создаем роутер
router = Router()

@router.callback_query(F.data == "create_event")
async def create_event(callback: types.CallbackQuery, state: FSMContext):
    logging.info(f"Пользователь {callback.from_user.id} начал создание события.")
    await state.set_state(EventState.WAITING_FOR_NAME)
    await callback.message.answer(
        "Введите название события:",
        reply_markup=create_reply_menu_keyboard()
    )

@router.message(F.text, EventState.WAITING_FOR_NAME)
async def process_event_name(message: types.Message, state: FSMContext):
    if message.text == "Вернуться в меню":
        await return_to_menu(message)
        return

    logging.info(f"Пользователь {message.from_user.id} ввел название события: {message.text}")
    await state.update_data(event_name=message.text)
    await state.set_state(EventState.WAITING_FOR_YEAR)
    await message.answer(
        "Выберите год:",
        reply_markup=create_year_keyboard()
    )


@router.callback_query(F.data.startswith("year_"), EventState.WAITING_FOR_YEAR)
async def process_year(callback: types.CallbackQuery, state: FSMContext):
    selected_year = int(callback.data.split("_")[1])
    logging.info(f"Пользователь {callback.from_user.id} выбрал год: {selected_year}")
    await state.update_data(event_year=selected_year)
    await state.set_state(EventState.WAITING_FOR_MONTH)
    await callback.message.answer(
        "Выберите месяц:",
        reply_markup=create_month_keyboard(selected_year)
    )

@router.callback_query(F.data.startswith("month_"), EventState.WAITING_FOR_MONTH)
async def process_month(callback: types.CallbackQuery, state: FSMContext):
    _, year, month = callback.data.split("_")
    selected_year = int(year)
    selected_month = int(month)
    logging.info(f"Пользователь {callback.from_user.id} выбрал месяц: {selected_month}")
    await state.update_data(event_month=selected_month)
    await state.set_state(EventState.WAITING_FOR_DAY)
    await callback.message.answer(
        "Выберите день:",
        reply_markup=create_day_keyboard(selected_year, selected_month))
    

@router.callback_query(F.data.startswith("day_"), EventState.WAITING_FOR_DAY)
async def process_day(callback: types.CallbackQuery, state: FSMContext):
    selected_date = callback.data.split("_")[1]
    logging.info(f"Пользователь {callback.from_user.id} выбрал дату: {selected_date}")
    await state.update_data(event_date=selected_date)
    await state.set_state(EventState.WAITING_FOR_TIME)
    await callback.message.answer(
        "Теперь выберите время:",
        reply_markup=create_time_keyboard())
    

@router.callback_query(F.data.startswith("time_"), EventState.WAITING_FOR_TIME)
async def process_time(callback: types.CallbackQuery, state: FSMContext):
    selected_time = callback.data.split("_")[1]
    logging.info(f"Пользователь {callback.from_user.id} выбрал время: {selected_time}")
    await state.update_data(event_time=selected_time)
    await state.set_state(EventState.WAITING_FOR_DESCRIPTION)
    await callback.message.answer(
        "Введите описание события (или пропустите, нажав /skip):",
        reply_markup=create_reply_menu_keyboard())
    

@router.callback_query(F.data == "custom_time", EventState.WAITING_FOR_TIME)
async def process_custom_time(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Введите время в формате ЧЧ:ММ (например, 14:30):",
        reply_markup=create_reply_menu_keyboard())
    
    await state.set_state(EventState.WAITING_FOR_CUSTOM_TIME)

@router.message(F.text, EventState.WAITING_FOR_CUSTOM_TIME)
async def process_custom_time_input(message: types.Message, state: FSMContext):
    try:
        # Проверяем, что время введено в правильном формате
        datetime.strptime(message.text, "%H:%M")
        await state.update_data(event_time=message.text)
        await state.set_state(EventState.WAITING_FOR_DESCRIPTION)
        await message.answer(
            "Введите описание события (или пропустите, нажав /skip):",
            reply_markup=create_reply_menu_keyboard())
        
    except ValueError:
        await message.answer(
            "Неверный формат времени. Введите время в формате ЧЧ:ММ (например, 14:30).",
            reply_markup=create_reply_menu_keyboard())
        

@router.message(Command("skip"), EventState.WAITING_FOR_DESCRIPTION)
async def skip_description(message: types.Message, state: FSMContext):
    logging.info(f"Пользователь {message.from_user.id} пропустил описание события.")
    await save_event(message, state)

@router.message(F.text, EventState.WAITING_FOR_DESCRIPTION)
async def process_event_description(message: types.Message, state: FSMContext):
    logging.info(f"Пользователь {message.from_user.id} ввел описание события: {message.text}")
    await state.update_data(event_description=message.text)
    await save_event(message, state)

async def save_event(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    event_name = user_data["event_name"]
    event_date = user_data["event_date"]
    event_time = user_data.get("event_time", "00:00")  # Время по умолчанию, если не указано
    event_description = user_data.get("event_description", "")

    # Объединяем дату и время
    event_datetime_str = f"{event_date} {event_time}"
    try:
        event_datetime = datetime.strptime(event_datetime_str, "%Y-%m-%d %H:%M")
    except ValueError:
        await message.answer(
            "Неверный формат даты или времени. Пожалуйста, попробуйте снова.",
            reply_markup=create_reply_menu_keyboard())
        return

    logging.info(f"Событие '{event_name}' создано пользователем {message.from_user.id}.")
    await add_event(message.from_user.id, event_name, event_description, event_datetime)
    await message.answer(
        f"Событие '{event_name}' успешно создано!",
        reply_markup=create_reply_menu_keyboard())

    # Планирование уведомления
    schedule_notification(message.from_user.id, event_datetime - timedelta(hours=1), event_name)

    # Очистка состояния
    await state.clear()

# Функция для регистрации хэндлеров
def register_create_event_handlers(dp):
    dp.include_router(router)