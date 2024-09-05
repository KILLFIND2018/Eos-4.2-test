import os
import logging
from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

TOKEN = '7220208121:AAFwXbn7zCCvuyHUPCA3iqeX9V4BsuQ54ec'
bot = TeleBot(TOKEN)

# Настройка логирования
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(filename='logs/telegram_bot.log', level=logging.INFO, 
                    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
logger = logging.getLogger(__name__)

# Получение URL из переменной окружения
RUNPOD_URL = "https://9ab7-169-150-196-133.ngrok-free.app"  # Обновите этот URL на текущий публичный URL ngrok

print("Bot is starting...")
logger.info("Bot is starting...")

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Support"))
    keyboard.add(KeyboardButton("Launch"))
    bot.send_message(message.chat.id, f'Hello {user.first_name}, my really friend!', reply_markup=keyboard)
    logger.info(f'Sent welcome message to {message.chat.id}')
    print(f"Sent welcome message to {message.chat.id}")

# Обработчик нажатий кнопок
@bot.message_handler(func=lambda message: True)
def on_click(message):
    text = message.text
    if text == 'Support':
        message_text = ("Since this project is not sponsored and the developer invests personal funds to maintain the server, "
                        "I have decided to limit the number of requests to 5. I would like to introduce you to the TONCOIN ecosystem, "
                        "a cryptocurrency created by the founder of Telegram. To increase the request limit, please contribute 0.3 TON. "
                        "This will also support the developer.")
        
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("Connect with me", url=f"{RUNPOD_URL}/connect"))
        bot.send_message(message.chat.id, message_text, reply_markup=keyboard)
        logger.info(f'Sent support message to {message.chat.id}')
        print(f"Sent support message to {message.chat.id}")
        
    elif text == 'Launch':
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("Welcome to EOs 3.0", url=f"{RUNPOD_URL}"))
        bot.send_message(message.chat.id, "Click here", reply_markup=keyboard)
        logger.info(f'Sent launch message to {message.chat.id}')
        print(f"Sent launch message to {message.chat.id}")

# Запуск бота
bot.polling(non_stop=True)
logger.info("Bot polling started...")
print("Bot polling started...")
