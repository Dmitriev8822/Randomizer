import telebot
from telebot import types
import random

# Замените на ваш токен от BotFather
BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    # Создаем кнопку для получения случайного числа
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_random = types.KeyboardButton('🎲 Получить случайное число')
    markup.add(btn_random)
    
    bot.send_message(
        message.chat.id, 
        f"Привет, {message.from_user.first_name}! Нажми на кнопку, чтобы получить случайное число.",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == '🎲 Получить случайное число')
def get_random_number(message):
    # Генерируем случайное число от 1 до 100
    random_number = random.randint(1, 100)
    bot.send_message(
        message.chat.id, 
        f"Ваше случайное число: **{random_number}**",
        parse_mode='Markdown'
    )

if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling()
