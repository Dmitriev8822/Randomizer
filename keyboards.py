from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Создаёт главную reply-клавиатуру с кнопками."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Выбрать из списка")],
            [KeyboardButton(text="Да / Нет")],
            [KeyboardButton(text="Монетка")],
            [KeyboardButton(text="Кубик")],
            [KeyboardButton(text="Команды")],
            [KeyboardButton(text="Помощь")],
        ],
        resize_keyboard=True,
    )
    return keyboard


def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    """Создаёт клавиатуру с кнопкой отмены."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Отмена")],
        ],
        resize_keyboard=True,
    )
    return keyboard
