import io
import asyncio
from dotenv import load_dotenv
from PIL import Image
import telebot
from telebot import types

from utils import clean_generated_caption
from common.common_properties import *
from machine_learning.captioning import CaptioningClass

load_dotenv()
bot_token = os.getenv("BOT_TOKEN")
if bot_token is None:
    print("Please set the BOT_TOKEN environment variable in the .env file")
    exit()

bot = telebot.TeleBot(bot_token)

captioning_class = CaptioningClass('captioning_model_5_epochs.h5')
user_states = {}


async def generate_and_send_caption(chat_id, image, user_id):
    generated_caption = captioning_class.generate_caption(image)

    cleaned_caption = clean_generated_caption(generated_caption)

    bot.send_message(chat_id, cleaned_caption)

    del user_states[user_id]


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button1 = types.KeyboardButton(team_button_message)
    button2 = types.KeyboardButton(metrics_button_message)
    button3 = types.KeyboardButton(photo_button_message)
    markup.row(button1, button2)
    markup.row(button3)
    bot.reply_to(message, "Welcome to Image Captioning Bot! Choose command to proceed", reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def handle_button_click(message):
    user_id = message.from_user.id
    if message.text == team_button_message:
        bot.send_message(message.chat.id, "Students of KN-312: Sviatoslav Oliinyk & Furdychka Nazar")
    elif message.text == photo_button_message:
        user_states[user_id] = wait_for_photo_command
        bot.send_message(message.chat.id, "Please, sent your photo for captioning")
    elif message.text == metrics_button_message:
        bot.send_message(message.chat.id, "HERE WILL BE METRICS")


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    user_id = message.from_user.id
    if user_id in user_states and user_states[user_id] == 'wait_for_photo':
        bot.send_message(message.chat.id, "Processing...")

        file_path = bot.get_file(message.photo[-1].file_id).file_path
        file = bot.download_file(file_path)
        image = Image.open(io.BytesIO(file))

        asyncio.run(generate_and_send_caption(message.chat.id, image, user_id))
    else:
        bot.reply_to(message, "Please, choose [Process photo] command first")

bot.polling()
