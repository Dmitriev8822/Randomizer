from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Создаёт главную reply-клавиатуру с кнопками."""
    
    buttons = [
        [KeyboardButton(text="Выбрать из списка")],
        [KeyboardButton(text="Да / Нет")],
        [KeyboardButton(text="Монетка")],
        [KeyboardButton(text="Кубик")],
        [KeyboardButton(text="Команды")],
        [KeyboardButton(text="Помощь")],
    ]
    
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=False
    )
