from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import random
from parser import parse_variants, split_teams
from keyboards import get_main_keyboard


router = Router()

# Ответы для /yesno
YESNO_ANSWERS = ["Да", "Нет", "Скорее да", "Скорее нет", "Позже", "Не сегодня"]


@router.message(F.text == "Выбрать из списка")
async def handle_choose_button(message: Message, state: FSMContext):
    """Обработка кнопки 'Выбрать из списка'"""
    await message.answer(
        "Отправьте список вариантов.\n"
        "Можно использовать запятые, слэши (/) или переносы строк.\n"
        "Пример: пицца, суши, бургер"
    )
    await state.set_state("waiting_for_variants")


@router.message(F.text == "Команды")
async def handle_teams_button(message: Message, state: FSMContext):
    """Обработка кнопки 'Команды'"""
    await message.answer(
        "Отправьте список участников.\n"
        "Можно использовать запятые или переносы строк.\n"
        "Пример: Анна, Борис, Виктор, Дарья"
    )
    await state.set_state("waiting_for_team_members")


@router.message(F.text == "Да / Нет")
async def handle_yesno_button(message: Message):
    """Обработка кнопки 'Да / Нет' - мгновенный ответ"""
    answer = random.choice(YESNO_ANSWERS)
    await message.answer(answer, reply_markup=get_main_keyboard())


@router.message(F.text == "Монетка")
async def handle_coin_button(message: Message):
    """Обработка кнопки 'Монетка' - мгновенный ответ"""
    result = random.choice(["Орёл", "Решка"])
    await message.answer(f"🪙 {result}", reply_markup=get_main_keyboard())


@router.message(F.text == "Кубик")
async def handle_dice_button(message: Message):
    """Обработка кнопки 'Кубик' - мгновенный ответ"""
    result = random.randint(1, 6)
    await message.answer(f"🎲 {result}", reply_markup=get_main_keyboard())


@router.message(F.text == "Помощь")
async def handle_help_button(message: Message):
    """Обработка кнопки 'Помощь'"""
    await send_help(message)


@router.message(F.text == "Команды")
async def handle_commands_button(message: Message):
    """Обработка кнопки 'Команды' - показ списка команд"""
    await send_help(message)


async def send_help(message: Message):
    """Отправляет справку по командам"""
    help_text = (
        "📚 *Справка по командам:*\n\n"
        "/start - Запустить бота и показать главное меню\n"
        "/help - Показать эту справку\n"
        "/choose - Выбрать случайный вариант из вашего списка\n"
        "/yesno - Получить ответ Да/Нет на ваш вопрос\n"
        "/coin - Подбросить монетку (Орёл/Решка)\n"
        "/dice - Бросить кубик (1-6)\n"
        "/teams - Разделить участников на 2 команды\n\n"
        "Также вы можете использовать кнопки в меню."
    )
    await message.answer(help_text, parse_mode="Markdown")


# Обработчик состояний для choose
@router.message(F.text, lambda msg: True)
async def handle_variants_input(message: Message, state: FSMContext):
    """Обработка ввода вариантов для /choose"""
    current_state = await state.get_state()
    
    if current_state == "waiting_for_variants":
        variants = parse_variants(message.text)
        
        if len(variants) < 2:
            await message.answer("Нужно минимум 2 варианта.", reply_markup=get_main_keyboard())
        else:
            chosen = random.choice(variants)
            await message.answer(f"Выбор: {chosen}", reply_markup=get_main_keyboard())
        
        await state.clear()
        return
    
    if current_state == "waiting_for_team_members":
        members = parse_variants(message.text)
        
        if len(members) < 2:
            await message.answer("Нужно минимум 2 участника.", reply_markup=get_main_keyboard())
        else:
            team1, team2 = split_teams(members)
            
            team1_text = "\n".join(f"- {member}" for member in team1)
            team2_text = "\n".join(f"- {member}" for member in team2)
            
            response = f"Команда 1:\n{team1_text}\n\nКоманда 2:\n{team2_text}"
            await message.answer(response, reply_markup=get_main_keyboard())
        
        await state.clear()
        return


# Обычные команды (не через кнопки)
@router.message(F.command("start"))
async def cmd_start(message: Message):
    """Команда /start"""
    welcome_text = (
        "👋 Привет! Я бот-рандомайзер.\n\n"
        "Я умею:\n"
        "• Выбирать случайный вариант из списка\n"
        "• Отвечать Да/Нет на вопросы\n"
        "• Подбрасывать монетку\n"
        "• Бросать кубик\n"
        "• Делить на команды"
    )
    await message.answer(welcome_text, reply_markup=get_main_keyboard())


@router.message(F.command("help"))
async def cmd_help(message: Message):
    """Команда /help"""
    await send_help(message)


@router.message(F.command("choose"))
async def cmd_choose(message: Message, state: FSMContext):
    """Команда /choose"""
    await message.answer(
        "Отправьте список вариантов.\n"
        "Можно использовать запятые, слэши (/) или переносы строк.\n"
        "Пример: пицца, суши, бургер"
    )
    await state.set_state("waiting_for_variants")


@router.message(F.command("yesno"))
async def cmd_yesno(message: Message):
    """Команда /yesno"""
    answer = random.choice(YESNO_ANSWERS)
    await message.answer(answer, reply_markup=get_main_keyboard())


@router.message(F.command("coin"))
async def cmd_coin(message: Message):
    """Команда /coin"""
    result = random.choice(["Орёл", "Решка"])
    await message.answer(f"🪙 {result}", reply_markup=get_main_keyboard())


@router.message(F.command("dice"))
async def cmd_dice(message: Message):
    """Команда /dice"""
    result = random.randint(1, 6)
    await message.answer(f"🎲 {result}", reply_markup=get_main_keyboard())


@router.message(F.command("teams"))
async def cmd_teams(message: Message, state: FSMContext):
    """Команда /teams"""
    await message.answer(
        "Отправьте список участников.\n"
        "Можно использовать запятые или переносы строк.\n"
        "Пример: Анна, Борис, Виктор, Дарья"
    )
    await state.set_state("waiting_for_team_members")
