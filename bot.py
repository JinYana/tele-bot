import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, Message
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


    elif call.data == "waitandsee":
        bot.send_message(call.message.chat.id,
                         "Patient might want to continue the medication for 2 days from the first loose stool to see if "
                         "there is any improvement. If there is still no improvement after 2 days, seek treatment from "
                         "a doctor or healthcare professional as soon as possible. Get well soon")

    elif call.data == "maybe more serious condition":
        diarrhoeasymptoms(call.message.chat.id)

    elif call.data == "more serious condition":
        bot.send_message(call.message.chat.id,
                         "Oh no! The symptoms might be a sign of a more serious condition. Be kindly advised to seek "
                         "treatment from a doctor or a healthcare professional as soon as possible. Get well soon")

    elif call.data == "got travel":
        travel(call.message.chat.id)

    elif call.data == "allergies":
        allergies(call.message.chat.id)

    elif call.data == "have allergy":
        bot.send_message(call.message.chat.id,
                         "Oh no! Patient might want to seek treatment from a doctor or healthcare professional as soon "
                         "as possible to prevent triggering any of the allergies from the medications. Get well soon!")

    elif call.data == "are you a breastfeeder":
        breastfeed(call.message.chat.id)

    elif call.data == "pregnant options":
        pregnantoptions(call.message.chat.id)

    elif call.data == "normal options":
        normaloptions(call.message.chat.id)

    elif call.data == "tablets":
        bot.send_message(call.message.chat.id,
                         "Brand Name: Ultracarbon \n"
                         "\n"
                         "Active Ingredient: Medicinal Charcoal \n"
                         "\n"
                         "Use For: Diarrhoea, Poisoning, Flatulence \n"
                         "\n"
                         "Dosing: 2 to 4 tablets, 3 to 4 times daily. Half the dosing is recommended for children. \n"
                         "\n"
                         "How It Works: Absorbs and remove toxins, bacteria, and noxious substances in the intestines. \n"
                         "\n"
                         "Common Side Effects: Vomiting, constipation, black stool. \n"
                         "\n"
                         "Note: Avoid dairy when taking the medication as it reduces the effectiveness of the medication. \n"
                         "\n"
                         "-Take with a full glass of water.-Space 2 hours apart with any other medications. \n"
                         "\n"
                         "-Stop medication once diarrhea stops or constipations happens. \n"
                         "\n"
                         "-Stop medication and see a doctor immediately when allergy symptoms such as rash, eye swelling"
                         " and difficulty in breathing occurs.")

    elif call.data == "capsules":
        bot.send_message(call.message.chat.id,
                         "Brand Name: Norit \n"
                         "Active Ingredient: Medicinal Charcoal \n"
                         "Use For: Diarrhoea, Poisoning, Flatulence \n"
                         "Dosing: 3 to 4 capsules, 3 times daily. \n"
                         "How It Works: Absorbs and remove toxins, bacteria, and noxious substances in the intestines. \n"
                         "Common Side Effects: Vomiting, constipation, black stool. \n"
                         "Note: -Avoid dairy when taking the medication as it reduces the effectiveness of the medication. \n"
                         "-Take with a full glass of water. \n"
                         "-Space 2 hours apart with any other medications. \n"
                         "-Stop medication once diarrhea stops or constipations happens. \n"
                         "-Stop medication and see a doctor immediately when allergy symptoms such as rash, eye swelling and difficulty in breathing occurs.")


@bot.message_handler(func=lambda call: True)
def answer(message: Message):
    if message.text == "Loperamide (Brand Name: Imodium)" \
            or message.text == "Diphenoxylate / Atropine (Brand Name: Dhamotil)" \
            or message.text == "Kaolin"\
            or message.text == "Medicinal Charcoal"\
            or message.text == "Dioctahedral Smectite (Brand Name: Smecta)":
        triedmedicineduration(message.chat.id)

    elif message.text == "Lactobacillus Acidophilus (Brand Name: Lacteol Forte)" \
        or message.text == "Oral Rehydration Salts (Brand Name: Hydralyte)" \
        or message.text == "Traditional Chinese Medicine" \
        or message.text == "No, I have not tried any diarrhoea medication yet":
        rawfood(message.chat.id)



#Diarrhoea bot
def age(message):
    keyboard = [

        [InlineKeyboardButton("Infant (0-1 Y.O.)", callback_data="unsuitable age")],

        [InlineKeyboardButton("Elderly (65 Y.O. and above)", callback_data="unsuitable age")],

        [InlineKeyboardButton("Children (2-17 Y.O.)", callback_data="how long diarrhoea")],

        [InlineKeyboardButton("Adult (18-64 Y.O.)", callback_data="how long diarrhoea")],

    ]
    bot.send_message(text="How old is the patient?", reply_markup=InlineKeyboardMarkup(keyboard), chat_id=message)


def triedmedicine(message):

    keyboard = [
        KeyboardButton("Loperamide (Brand Name: Imodium)"),

         KeyboardButton("Diphenoxylate / Atropine (Brand Name: Dhamotil)"),

         KeyboardButton("Kaolin"),

         KeyboardButton("Medicinal Charcoal"),

         KeyboardButton("Dioctahedral Smectite (Brand Name: Smecta)"),

         KeyboardButton("Lactobacillus Acidophilus (Brand Name: Lacteol Forte)"),

         KeyboardButton("Oral Rehydration Salts (Brand Name: Hydralyte)"),

         KeyboardButton("Traditional Chinese Medicine"),

         KeyboardButton("No, I have not tried any diarrhoea medication yet")
    ]
    mark = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for i in keyboard:
        mark.add(i)
    bot.send_message(text="Have you tried any of the diarrhoea medication below?", reply_markup=mark, chat_id=message)

def howlong(message):
    keyboard = [
        [InlineKeyboardButton("More than 3 days", callback_data="serious diarrhoea")],
                [InlineKeyboardButton("Less than 3 days", callback_data="which medincine have been tried")],
    ]
    bot.send_message(text="How long has the diarrhoea lasted?", reply_markup=InlineKeyboardMarkup(keyboard), chat_id=message)


def triedmedicineduration(message):
    keyboard = [
        [InlineKeyboardButton("Less than 2 days", callback_data="waitandsee")],
        [InlineKeyboardButton("More than 2 days", callback_data="serious diarrhoea")],
    ]
    bot.send_message(text="How long has the diarrhoea lasted?", reply_markup=InlineKeyboardMarkup(keyboard), chat_id=message)


def rawfood(message):

    keyboard = [
        [InlineKeyboardButton("Yes", callback_data="maybe more serious condition")],
        [InlineKeyboardButton("No", callback_data="got travel")],
    ]
    bot.send_message(text="Have you eaten anything raw or undercooked recently?", reply_markup=InlineKeyboardMarkup(keyboard), chat_id=message)

def diarrhoeasymptoms(message):

    keyboard = [
        [InlineKeyboardButton("Yes", callback_data="more serious condition")],
        [InlineKeyboardButton("No", callback_data="got travel")],
    ]
    bot.send_message(text="Have the patient displayed any of the symptoms below? \n"
                          "\n"
                          "For adults: \n"
                          "-Black sticky or bloody stools \n"
                          "-Fever above 39 degrees Celsius \n"
                          "-Severe pain in the stomach or anus area \n"
                          "-Symptoms of dehydration such as little or no urine, dark colored-urine, weakness, dizziness, lightheadedness, dry mouth, or skin \n"
                          "\n"
                          "For children: \n"
                          "-Black sticky or bloody stools \n"
                          "-Severe pain in the stomach or anus area \n"
                          "-Sunken stomach, eyes or cheeks \n"
                          "-Sleepy or unresponsive-Cries with no tears or dry mouth \n"
                          "Symptoms of dehydration such as little or no urine, dark colored-urine, weakness, dizziness, lightheadedness, dry mouth, or skin",
                     reply_markup=InlineKeyboardMarkup(keyboard), chat_id=message)

def travel(message):

    keyboard = [
        [InlineKeyboardButton("Yes", callback_data="allergies")],
        [InlineKeyboardButton("No", callback_data="more serious condition")],
    ]
    bot.send_message(text="Have you travelled for the past week?", reply_markup=InlineKeyboardMarkup(keyboard), chat_id=message)


def allergies(message):
    keyboard = [
        [InlineKeyboardButton("Yes", callback_data="have allergy")],
        [InlineKeyboardButton("No", callback_data="are you a breastfeeder")],
    ]
    bot.send_message(text="Are you allergic to any of the medication below?\n"
                          "\n"
                          "-Aluminum Silicates \n"
                          "-Medicinal Charcoal \n"
                          "-Dioctahedral Smectite (Brand Name: Smecta)", reply_markup=InlineKeyboardMarkup(keyboard),
                     chat_id=message)

def breastfeed(message):
    keyboard = [
        [InlineKeyboardButton("Yes", callback_data="pregnant options")],
        [InlineKeyboardButton("No", callback_data="normal options")],
    ]
    bot.send_message(text="Are you current pregnant or breastfeeding?", reply_markup=InlineKeyboardMarkup(keyboard),
                     chat_id=message)

def normaloptions(message):
    keyboard = [
        [InlineKeyboardButton("Liquid", callback_data="liquid")],
        [InlineKeyboardButton("Tablets", callback_data="tablets")],
        [InlineKeyboardButton("Capsules", callback_data="capsules")],
        [InlineKeyboardButton("Powder Sachets", callback_data="powder")],
        [InlineKeyboardButton("No Preference", callback_data="tablets")],
    ]
    bot.send_message(text="What kind of medicine would you prefer?", reply_markup=InlineKeyboardMarkup(keyboard),
                     chat_id=message)


def pregnantoptions(message):
    keyboard = [
        [InlineKeyboardButton("Liquid", callback_data="liquid")],
        [InlineKeyboardButton("Tablets", callback_data="tablets")],
        [InlineKeyboardButton("Capsules", callback_data="capsules")],
        [InlineKeyboardButton("No Preference", callback_data="tablets")],
    ]
    bot.send_message(text="What kind of medicine would you prefer?", reply_markup=InlineKeyboardMarkup(keyboard),
                     chat_id=message)


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
















