from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton

def create_reply_menu_keyboard():
    """Создает Reply-кнопку для выхода в меню."""
    builder = ReplyKeyboardBuilder()

    # Добавляем кнопку
    builder.button(text="Вернуться в меню")

    # Возвращаем клавиатуру
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)