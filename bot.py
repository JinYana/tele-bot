import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import os
from flask import Flask, request


server = Flask(__name__)

API_KEY = "5324891918:AAGKD1WX7zyIlX3aLKr-GAICBjenjsH-1Mg"
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = [
        [InlineKeyboardButton("Recommend Medicine", callback_data="rec"),]
    ]
    bot.send_message(text="Hi what can we do for you?", reply_markup=InlineKeyboardMarkup(keyboard), chat_id=message.chat.id)
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "rec":
        med(call.message.chat.id)
    elif call.data == "yes":
        bot.send_message(call.message.chat.id,
                         "Please got to a doctor as I am not qualfied to recommend medicine to you")


    elif call.data == "no":
        noallergies(call.message.chat.id)



def med(message):
    keyboard = [
        [InlineKeyboardButton("Yes", callback_data="yes"),
                InlineKeyboardButton("No", callback_data="no"),]
    ]
    bot.send_message(text="Do You Have Any Allergies?", reply_markup=InlineKeyboardMarkup(keyboard), chat_id=message)


def noallergies(message):
    bot.send_message(text="I recommend Zhu Ge Liang:", chat_id=message)
    bot.send_photo(photo="https://imgur.com/ac5G9TS", chat_id=message)



@server.route('/' + API_KEY, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://pharmacy-botty.herokuapp.com/' + API_KEY)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
















