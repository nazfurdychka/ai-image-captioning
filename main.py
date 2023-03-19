import telebot
from telebot import types
import os
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")

if bot_token is None:
    print("Please set the BOT_TOKEN environment variable in the .env file")
    exit()

bot = telebot.TeleBot(bot_token)

team_button_message = 'Get information about team'
photo_button_message = 'Process photo'


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button1 = types.KeyboardButton(team_button_message)
    button2 = types.KeyboardButton(photo_button_message)
    markup.row(button1, button2)
    bot.reply_to(message, "Welcome to my bot! Choose command to proceed", reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def handle_button_click(message):
    if message.text == team_button_message:
        bot.send_message(message.chat.id, "Amazing team")
    elif message.text == photo_button_message:
        bot.send_message(message.chat.id, "Send photo....")


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    file_path = file_info.file_path

    file = bot.download_file(file_path)

    size = len(file)

    bot.send_message(message.chat.id, f'The size of the photo is {size} bytes')


bot.polling()
