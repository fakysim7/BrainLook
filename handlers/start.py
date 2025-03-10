from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import logging
from aiogram.types import FSInputFile

from utils.states import ProfileStates
from keyboards.menu import create_main_menu_keyboard
from keyboards.profile_menu import create_profile_menu_keyboard
from database.crud import Database

# Создаем роутер
router = Router()

# Стейты для FSM
class Registration(StatesGroup):
    age = State()
    workplace = State()

@router.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    logging.info(f"Пользователь {message.from_user.id} запустил бота.")
    
    # Подключаемся к базе данных
    db = Database()
    await db.connect()
    
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    
    # Проверяем, зарегистрирован ли пользователь
    user_info = await db.get_user_info(user_id)
    if not user_info:
        # Если пользователь не зарегистрирован, запрашиваем возраст
        await message.answer("Привет! Для регистрации укажи свой возраст:")
        await state.set_state(Registration.age)
    else:
        # Если пользователь уже зарегистрирован, приветствуем его
        await message.answer(
            f"Привет, {first_name}! Выбери действие:",
            reply_markup=create_main_menu_keyboard()
        )
    
    await db.close()

@router.message(Registration.age)
async def process_age(message: types.Message, state: FSMContext):
    # Сохраняем возраст
    age = message.text
    if not age.isdigit():
        await message.answer("Пожалуйста, введите возраст числом.")
        return
    
    await state.update_data(age=int(age))
    
    # Запрашиваем место работы/учебы
    await message.answer("Теперь укажи место работы или учебы:")
    await state.set_state(Registration.workplace)

@router.message(Registration.workplace)
async def process_workplace(message: types.Message, state: FSMContext):
    # Сохраняем место работы/учебы
    workplace = message.text
    await state.update_data(workplace=workplace)
    
    # Получаем все данные из состояния
    data = await state.get_data()
    age = data.get("age")
    workplace = data.get("workplace")
    
    # Регистрируем пользователя
    db = Database()
    await db.connect()
    
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    
    await db.register_user(user_id, username, first_name, last_name, age, workplace)
    await db.close()
    
    # Завершаем состояние
    await state.clear()
    
    # Приветствуем пользователя
    await message.answer(
        "Регистрация завершена! Выбери действие:",
        reply_markup=create_main_menu_keyboard()
    )

@router.callback_query(F.data == "profile")
async def profile(callback: types.CallbackQuery):
    db = Database()
    await db.connect()
    
    user_id = callback.from_user.id
    user_info = await db.get_user_info(user_id)
    await db.close()
    
    if user_info:
        # Обработка NULL в last_name
        last_name = user_info['last_name'] if user_info['last_name'] else "Не указано"
        
        profile_message = (
            f"👤 Профиль:\n\n"
            f"Имя: {user_info['first_name']}\n\n"
            f"Фамилия: {last_name}\n\n"
            f"Возраст: {user_info['age']}\n\n"
            f"Место работы/учебы: {user_info['workplace']}"
        )
        await callback.answer()
        await callback.message.answer(profile_message, reply_markup=create_profile_menu_keyboard())
    else:
        await callback.message.answer("Профиль не найден. Пожалуйста, зарегистрируйтесь с помощью команды /start.")

@router.callback_query(F.data == "return_to_menu")
async def return_to_menu(callback: types.CallbackQuery):
    logging.info(f"Пользователь {callback.message.from_user.id} вернулся в меню.")
    photo = FSInputFile("D:/BraiLook/AI_Assist/image/image.png")
    await callback.answer()
    await callback.message.answer_photo(
        photo,
        "Выбери действие:",
        reply_markup=create_main_menu_keyboard()
    )

@router.callback_query(F.data == "change_age")
async def change_age(callback: types.CallbackQuery, state: FSMContext):
    """Запрашивает новый возраст."""
    await callback.message.answer("Введите ваш новый возраст:")
    await state.set_state(ProfileStates.change_age)

@router.message(ProfileStates.change_age)
async def process_new_age(message: types.Message, state: FSMContext):
    """Обрабатывает новый возраст и обновляет его в базе данных."""
    age = message.text
    if not age.isdigit():
        await message.answer("Пожалуйста, введите возраст числом.")
        return
    
    # Обновляем возраст в базе данных
    db = Database()
    await db.connect()
    await db.update_user_age(message.from_user.id, int(age))
    await db.close()
    
    await message.answer("Возраст успешно обновлен!")
    await state.clear()

@router.callback_query(F.data == "change_workplace")
async def change_workplace(callback: types.CallbackQuery, state: FSMContext):
    """Запрашивает новое место работы/учебы."""
    await callback.message.answer("Введите ваше новое место работы/учебы:")
    await state.set_state(ProfileStates.change_workplace)


@router.message(ProfileStates.change_workplace)
async def process_new_workplace(message: types.Message, state: FSMContext):
    """Обрабатывает новое место работы/учебы и обновляет его в базе данных."""
    workplace = message.text
    
    # Обновляем место работы/учебы в базе данных
    db = Database()
    await db.connect()
    await db.update_user_workplace(message.from_user.id, workplace)
    await db.close()
    
    await message.answer("Место работы/учебы успешно обновлено!")
    await state.clear()

@router.message(F.text == "Вернуться в меню")
async def return_to_menu(message: types.Message):
    logging.info(f"Пользователь {message.from_user.id} вернулся в меню.")
    photo = FSInputFile("D:/BraiLook/AI_Assist/image/image.png")
    await message.answer_photo(
        photo,
        "Выбери действие:",
        reply_markup=create_main_menu_keyboard()
    )


# Функция для регистрации хэндлеров
def register_start_handlers(dp):
    dp.include_router(router)
