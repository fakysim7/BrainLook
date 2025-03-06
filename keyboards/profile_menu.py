from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def create_profile_menu_keyboard():
    """Создает inline-клавиатуру меню профиля."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Изменить возраст", callback_data="change_age")],
            [InlineKeyboardButton(text="Изменить место работы/учебы", callback_data="change_workplace")],
            [InlineKeyboardButton(text="Вернуться в меню", callback_data="return_to_menu")],
        ],
    )
    return keyboard