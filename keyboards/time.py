from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from datetime import datetime


def create_time_keyboard():
    builder = InlineKeyboardBuilder()

    # Предлагаем стандартные варианты времени
    times = ["09:00", "12:00", "15:00", "18:00", "21:00"]
    for time in times:
        builder.button(text=time, callback_data=f"time_{time}")

    # Добавляем кнопку для ввода своего времени
    builder.button(text="Свое время", callback_data="custom_time")

    # Располагаем кнопки в 2 столбца
    builder.adjust(2)
    return builder.as_markup()
