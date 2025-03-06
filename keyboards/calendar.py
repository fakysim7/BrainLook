from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from datetime import datetime

def create_year_keyboard():
    """Создает клавиатуру для выбора года."""
    builder = InlineKeyboardBuilder()
    current_year = datetime.now().year
    for year in range(current_year, current_year + 5):  # Предлагаем 5 лет вперед
        builder.button(text=str(year), callback_data=f"year_{year}")
    builder.adjust(3)  # Располагаем кнопки в 3 столбца
    return builder.as_markup()

def create_month_keyboard(year: int):
    """Создает клавиатуру для выбора месяца."""
    builder = InlineKeyboardBuilder()
    months = [
        "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
        "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
    ]
    for i, month in enumerate(months, start=1):
        builder.button(text=month, callback_data=f"month_{year}_{i}")
    builder.adjust(3)  # Располагаем кнопки в 3 столбца
    return builder.as_markup()

def create_day_keyboard(year: int, month: int):
    """Создает клавиатуру для выбора дня."""
    builder = InlineKeyboardBuilder()
    # Определяем количество дней в месяце
    if month == 2:  # Февраль
        days = 29 if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) else 28
    elif month in [4, 6, 9, 11]:  # Апрель, Июнь, Сентябрь, Ноябрь
        days = 30
    else:  # Остальные месяцы
        days = 31

    for day in range(1, days + 1):
        builder.button(text=str(day), callback_data=f"day_{year}-{month:02d}-{day:02d}")
    builder.adjust(7)  # Располагаем кнопки в 7 столбцов (как в календаре)
    return builder.as_markup()

