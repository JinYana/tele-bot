import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
import os
from flask import Flask, request


server = Flask(__name__)

API_KEY = "5324891918:AAGKD1WX7zyIlX3aLKr-GAICBjenjsH-1Mg"
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = [
        [InlineKeyboardButton("I need help with diarrhoea!", callback_data="rec"),]
    ]
    bot.send_message(text="Hi what can we do for you?", reply_markup=InlineKeyboardMarkup(keyboard), chat_id=message.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "rec":
        age(call.message.chat.id)
    elif call.data == "unsuitable age":
        bot.send_message(call.message.chat.id,
                         "Oh no! Due to the age, patient is at high risk of developing complications due to diarrhoea. Be kindly advised to seek treatment from a doctor or a healthcare professional as soon as possible. Get well soon!")

    elif call.data == "how long diarrhoea":
        howlong(call.message.chat.id)

    elif call.data == "serious diarrhoea":
        bot.send_message(call.message.chat.id,
                         "Oh no! The diarrhoea seems to be much more serious than expected. Be kindly advised to seek "
                         "treatment from a doctor or a healthcare professional as soon as possible. Get well soon!")

    elif call.data == "which medincine have been tried":
        triedmedicine(call.message.chat.id)

    elif call.data == "Diarrhoea medicine how long":
        triedmedicineduration(call.message.chat.id)

    elif call.data == "waitandsee":
        bot.send_message(call.message.chat.id,
                         "Patient might want to continue the medication for 2 days from the first loose stool to see if "
                         "there is any improvement. If there is still no improvement after 2 days, seek treatment from "
                         "a doctor or healthcare professional as soon as possible. Get well soon")

    elif call.data == "got eat raw food":
        rawfood(call.message.chat.id)

    elif call.data == "more serious condition":
        bot.send_message(call.message.chat.id,
                         "Oh no! The symptoms might be a sign of a more serious condition. Be kindly advised to seek "
                         "treatment from a doctor or a healthcare professional as soon as possible. Get well soon")
    elif call.data == "got travel":
        travel(call.message.chat.id)





#Diarrhoea bot
def age(message):
    keyboard = [
        [InlineKeyboardButton("Infant (0-1 Y.O.)", callback_data="unsuitable age"),
                InlineKeyboardButton("Elderly (65 Y.O. and above)", callback_data="unsuitable age"),
         InlineKeyboardButton("Children (2-17 Y.O.)", callback_data="how long diarrhoea"),
         InlineKeyboardButton("Adult (18-64 Y.O.)", callback_data="how long diarrhoea"),]
    ]
    bot.send_message(text="How old is the patient?", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True), chat_id=message)


def triedmedicine(message):
    keyboard = [
        [InlineKeyboardButton("Loperamide (Brand Name: Imodium)", callback_data="Diarrhoea medicine how long"),
         InlineKeyboardButton("Diphenoxylate / Atropine (Brand Name: Dhamotil)", callback_data="Diarrhoea medicine how long"),
         InlineKeyboardButton("Kaolin", callback_data="Diarrhoea medicine how long"),
         InlineKeyboardButton("Medicinal Charcoal", callback_data="Diarrhoea medicine how long"),
         InlineKeyboardButton("Dioctahedral Smectite (Brand Name: Smecta)", callback_data="Diarrhoea medicine how long"),
         InlineKeyboardButton("Lactobacillus Acidophilus (Brand Name: Lacteol Forte)", callback_data="got eat raw food"),
         InlineKeyboardButton("Oral Rehydration Salts (Brand Name: Hydralyte)", callback_data="got eat raw food"),
         InlineKeyboardButton("Traditional Chinese Medicine", callback_data="got eat raw food"),
         InlineKeyboardButton("No, I have not tried any diarrhoea medication yet", callback_data="got eat raw food"),]
    ]
    bot.send_message(text="How long has the diarrhoea lasted?", reply_markup=InlineKeyboardMarkup(keyboard), chat_id=message)

def howlong(message):
    keyboard = [
        [InlineKeyboardButton("More than 3 days", callback_data="serious diarrhoea"),
                InlineKeyboardButton("Less than 3 days", callback_data="which medincine have been tried"),]
    ]
    bot.send_message(text="How long has the diarrhoea lasted?", reply_markup=InlineKeyboardMarkup(keyboard), chat_id=message)


def triedmedicineduration(message):
    keyboard = [
        [InlineKeyboardButton("Less than 2 days", callback_data="waitandsee"),
        InlineKeyboardButton("More than 2 days", callback_data="serious diarrhoea"), ]
    ]
    bot.send_message(text="How long has the diarrhoea lasted?", reply_markup=InlineKeyboardMarkup(keyboard), chat_id=message)


def rawfood(message):

    keyboard = [
        [InlineKeyboardButton("Yes", callback_data="more serious condition"),
        InlineKeyboardButton("No", callback_data="got travel"), ]
    ]
    bot.send_message(text="How long has the diarrhoea lasted?", reply_markup=InlineKeyboardMarkup(keyboard), chat_id=message)

def travel(message):

    keyboard = [
        [InlineKeyboardButton("Yes", callback_data="more serious condition"),
        InlineKeyboardButton("No", callback_data="got travel"), ]
    ]
    bot.send_message(text="How long has the diarrhoea lasted?", reply_markup=InlineKeyboardMarkup(keyboard), chat_id=message)





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















