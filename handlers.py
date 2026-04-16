from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import random

from keyboards import get_main_keyboard, get_cancel_keyboard
from parser import parse_variants, split_teams

router = Router()


# === Ответы для /yesno ===
YESNO_ANSWERS = [
    "Да",
    "Нет",
    "Скорее да",
    "Скорее нет",
    "Позже",
    "Не сегодня",
]

# === Ответы для /coin ===
COIN_ANSWERS = ["Орёл", "Решка"]


@router.message(F.text == "/start")
async def cmd_start(message: Message):
    """Обработчик команды /start."""
    text = (
        "Привет! Я бот-рандомайзер.\n\n"
        "Что я умею:\n"
        "• Выбрать случайный вариант из вашего списка\n"
        "• Ответить Да/Нет на ваш вопрос\n"
        "• Подбросить монетку (Орёл/Решка)\n"
        "• Бросить кубик (1-6)\n"
        "• Разделить участников на 2 команды\n\n"
        "Выберите действие в меню ниже:"
    )
    await message.answer(text, reply_markup=get_main_keyboard())


@router.message(F.text == "/help")
async def cmd_help(message: Message):
    """Обработчик команды /help."""
    text = (
        "📖 Инструкция по использованию бота:\n\n"
        "Команды:\n"
        "/start - Запустить бота и показать меню\n"
        "/choose - Выбрать случайный вариант из списка (отправьте варианты через запятую, / или с новой строки)\n"
        "/yesno - Получить ответ Да/Нет на ваш вопрос\n"
        "/coin - Подбросить монетку (Орёл/Решка)\n"
        "/dice - Бросить кубик (1-6)\n"
        "/teams - Разделить участников на 2 команды\n"
        "/help - Показать эту инструкцию\n\n"
        "Примеры:\n"
        "• пицца, суши, бургер\n"
        "• фильм 1 / фильм 2 / фильм 3\n"
        "• вариант 1\\nвариант 2\\nвариант 3"
    )
    await message.answer(text)


@router.message(F.text == "Помощь")
async def btn_help(message: Message):
    """Обработчик кнопки Помощь."""
    await cmd_help(message)


@router.message(F.text == "/yesno")
async def cmd_yesno(message: Message):
    """Обработчик команды /yesno."""
    answer = random.choice(YESNO_ANSWERS)
    await message.answer(answer)


@router.message(F.text == "Да / Нет")
async def btn_yesno(message: Message):
    """Обработчик кнопки Да / Нет."""
    await cmd_yesno(message)


@router.message(F.text == "/coin")
async def cmd_coin(message: Message):
    """Обработчик команды /coin."""
    answer = random.choice(COIN_ANSWERS)
    await message.answer(answer)


@router.message(F.text == "Монетка")
async def btn_coin(message: Message):
    """Обработчик кнопки Монетка."""
    await cmd_coin(message)


@router.message(F.text == "/dice")
async def cmd_dice(message: Message):
    """Обработчик команды /dice."""
    result = random.randint(1, 6)
    await message.answer(f"🎲 {result}")


@router.message(F.text == "Кубик")
async def btn_dice(message: Message):
    """Обработчик кнопки Кубик."""
    await cmd_dice(message)


# === FSM состояния ===
class ChooseState:
    waiting_for_variants = "waiting_for_variants"


class TeamsState:
    waiting_for_members = "waiting_for_members"


@router.message(F.text == "/choose")
async def cmd_choose(message: Message, state: FSMContext):
    """Обработчик команды /choose - запрашивает список вариантов."""
    await state.set_state(ChooseState.waiting_for_variants)
    await message.answer(
        "Отправьте список вариантов через запятую, / или с новой строки.\n"
        "Например: пицца, суши, бургер",
        reply_markup=get_cancel_keyboard(),
    )


@router.message(F.text == "Выбрать из списка")
async def btn_choose(message: Message, state: FSMContext):
    """Обработчик кнопки Выбрать из списка."""
    await cmd_choose(message, state)


@router.message(F.text == "Отмена")
async def cancel_handler(message: Message, state: FSMContext):
    """Отменяет текущее состояние."""
    await state.clear()
    await message.answer(
        "Действие отменено.",
        reply_markup=get_main_keyboard(),
    )


@router.message(F.state == ChooseState.waiting_for_variants)
async def process_variants(message: Message, state: FSMContext):
    """Обрабатывает список вариантов и выбирает случайный."""
    text = message.text
    
    variants = parse_variants(text)
    
    if len(variants) < 2:
        await message.answer("Нужно минимум 2 варианта.")
        return
    
    choice = random.choice(variants)
    await message.answer(f"Выбор: {choice}", reply_markup=get_main_keyboard())
    await state.clear()


@router.message(F.text == "/teams")
async def cmd_teams(message: Message, state: FSMContext):
    """Обработчик команды /teams - запрашивает список участников."""
    await state.set_state(TeamsState.waiting_for_members)
    await message.answer(
        "Отправьте список участников через запятую или с новой строки.\n"
        "Например: Анна, Борис, Виктор, Дарья",
        reply_markup=get_cancel_keyboard(),
    )


@router.message(F.text == "Команды")
async def btn_teams(message: Message, state: FSMContext):
    """Обработчик кнопки Команды."""
    await cmd_teams(message, state)


@router.message(F.state == TeamsState.waiting_for_members)
async def process_teams(message: Message, state: FSMContext):
    """Обрабатывает список участников и делит на 2 команды."""
    text = message.text
    
    members = parse_variants(text)
    
    if len(members) < 2:
        await message.answer("Нужно минимум 2 участника.")
        return
    
    team1, team2 = split_teams(members)
    
    # Формируем ответ
    team1_text = "\n".join(f"- {m}" for m in team1)
    team2_text = "\n".join(f"- {m}" for m in team2)
    
    response = f"Команда 1:\n{team1_text}\n\nКоманда 2:\n{team2_text}"
    
    await message.answer(response, reply_markup=get_main_keyboard())
    await state.clear()
