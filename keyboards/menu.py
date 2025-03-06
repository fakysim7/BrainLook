from aiogram.utils.keyboard import InlineKeyboardBuilder

def create_main_menu_keyboard():
    """Создает главное меню с Inline-кнопками."""
    builder = InlineKeyboardBuilder()

    # Добавляем кнопки
    builder.button(text="Создать событие", callback_data="create_event")
    builder.button(text="Мои события", callback_data="my_events")
    builder.button(text="Консультация", callback_data="consult")
    builder.button(text="Профиль", callback_data="profile")

    # Располагаем кнопки в один столбец
    builder.adjust(1)
    return builder.as_markup()