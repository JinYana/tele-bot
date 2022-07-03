import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, Message, \
    ReplyKeyboardRemove
import os
from flask import Flask, request, Response

server = Flask(__name__)

API_KEY = "5324891918:AAGKD1WX7zyIlX3aLKr-GAICBjenjsH-1Mg"
bot = telebot.TeleBot(API_KEY)

global currentmsgid

currentmsgid = ""

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = [
        [InlineKeyboardButton("I need help with diarrhoea!", callback_data="rec"), ]
    ]
    bot.send_message(text="Hi what can we do for you?", reply_markup=InlineKeyboardMarkup(keyboard),
                     chat_id=message.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call, currentmsgid=None):

    if call.data == "rec" and call.message.chat.id != currentmsgid:
        age(call.message.chat.id)



    # elif call.data == "yes":
    #     jerod2(call.message.chat.id)
    #
    # elif call.data == "no":
    #     age(call.message.chat.id)

    elif call.data == "unsuitable age" and call.message.chat.id != currentmsgid:
        bot.send_message(call.message.chat.id,
                         "Oh no! Due to the age, patient is at high risk of developing complications due to diarrhoea. Be kindly advised to seek treatment from a doctor or a healthcare professional as soon as possible. Get well soon!")
        bot.answer_callback_query(call.id, "hi")

    elif call.data == "how long diarrhoea" and call.message.chat.id != currentmsgid:
        howlong(call.message.chat.id)
        bot.answer_callback_query(call.id, "hi")

    elif call.data == "serious diarrhoea" and call.message.chat.id != currentmsgid:
        bot.send_message(call.message.chat.id,
                         "Oh no! The diarrhoea seems to be much more serious than expected. Be kindly advised to seek "
                         "treatment from a doctor or a healthcare professional as soon as possible. Get well soon!")
        bot.answer_callback_query(call.id, "hi")



    elif call.data == "which medincine have been tried" and call.message.chat.id != currentmsgid:
        triedmedicine(call.message.chat.id)


    elif call.data == "waitandsee" and call.message.chat.id != currentmsgid:
        bot.send_message(call.message.chat.id,
                         "You might want to continue the medication for 2 days from the first loose stool to see if "
                         "there is any improvement. If there is still no improvement after 2 days, seek treatment from "
                         "a doctor or healthcare professional as soon as possible. Get well soon")
        bot.answer_callback_query(call.id, "hi")
        bot.stop_polling()

    elif call.data == "maybe more serious condition" and call.message.chat.id != currentmsgid:
        diarrhoeasymptoms1(call.message.chat.id)

    elif call.data == "diarrhoeasymptoms2" and call.message.chat.id != currentmsgid:
        diarrhoeasymptoms2(call.message.chat.id)

    elif call.data == "more serious condition" and call.message.chat.id != currentmsgid:
        bot.send_message(call.message.chat.id,
                         "Oh no! The symptoms might be a sign of a more serious condition. Be kindly advised to seek "
                         "treatment from a doctor or a healthcare professional as soon as possible. Get well soon")
        bot.answer_callback_query(call.id, "hi")


    elif call.data == "got travel" and call.message.chat.id != currentmsgid:
        travel(call.message.chat.id)

    elif call.data == "got travel2" and call.message.chat.id != currentmsgid:
        travel2(call.message.chat.id)

    elif call.data == "allergies" and call.message.chat.id != currentmsgid:
        allergies(call.message.chat.id)

    elif call.data == "have allergy" and call.message.chat.id != currentmsgid:
        bot.send_message(call.message.chat.id,
                         "Oh no! You might want to seek treatment from a doctor or healthcare professional as soon "
                         "as possible to prevent triggering any of the allergies from the medications. Get well soon!")
        bot.answer_callback_query(call.id, "hi")

    elif call.data == "are you a breastfeeder" and call.message.chat.id != currentmsgid:
        breastfeed(call.message.chat.id)

    elif call.data == "pregnant options" and call.message.chat.id != currentmsgid:
        pregnantoptions(call.message.chat.id)

    elif call.data == "normal options" and call.message.chat.id != currentmsgid:
        normaloptions(call.message.chat.id)

    elif call.data == "tablets" and call.message.chat.id != currentmsgid:
        bot.send_photo(chat_id=call.message.chat.id, photo="https://imgur.com/DvjpvEN",
                       caption="We recommend using Ultracarbon"
                               "\n"
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
                               "Note: \n"
                               "-Avoid dairy when taking the medication as it reduces the effectiveness of the medication. \n"
                               "\n"
                               "-Take with a full glass of water.-Space 2 hours apart with any other medications. \n"
                               "\n"
                               "-Stop medication once diarrhea stops or constipations happens. \n"
                               "\n"
                               "-Stop medication and see a doctor immediately when allergy symptoms such as rash, eye swelling"
                               " and difficulty in breathing occurs.", )

        bot.answer_callback_query(call.id, "hi")



    elif call.data == "capsules" and call.message.chat.id != currentmsgid:
        bot.send_photo(chat_id=call.message.chat.id, photo="https://imgur.com/DvjpvEN",
                       caption="We recommend using Norit\n"
                               "Brand Name: Norit \n"
                               "\n"
                               "Active Ingredient: Medicinal Charcoal \n"
                               "\n"
                               "Use For: Diarrhoea, Poisoning, Flatulence \n"
                               "\n"
                               "Dosing: 3 to 4 capsules, 3 times daily. \n"
                               "\n"
                               "How It Works: Absorbs and remove toxins, bacteria, and noxious substances in the intestines. \n"
                               "\n"
                               "Common Side Effects: Vomiting, constipation, black stool. \n"
                               "\n"
                               "Note: \n"
                               "-Avoid dairy when taking the medication as it reduces the effectiveness of the medication. \n"
                               "\n"
                               "-Take with a full glass of water. \n"
                               "\n"
                               "-Space 2 hours apart with any other medications. \n"
                               "\n"
                               "-Stop medication once diarrhea stops or constipations happens. \n"
                               "\n"
                               "-Stop medication and see a doctor immediately when allergy symptoms such as rash, eye swelling and difficulty in breathing occurs.")
        bot.answer_callback_query(call.id, "hi")


    elif call.data == "liquid" and call.message.chat.id != currentmsgid:
        bot.send_photo(chat_id=call.message.chat.id, photo="https://imgur.com/DvjpvEN",
                       caption="We recommend using Kaomix\n"
                               "Brand Name: Kaomix \n"
                               "\n"
                               "Active Ingredient: Aluminum Silicates \n"
                               "\n"
                               "Use For: Diarrhoea \n"
                               "\n"
                               "Dosing: Children 3 to 5 Y.O. (3 to 5ml), Children 6 to 12 Y.O. (10 to 20ml). \n"
                               "\n"
                               "Adults and Children over 12 Y.O. (20 to 40ml). \n"
                               "\n"
                               "How It Works: Absorbs and remove toxins, bacteria, and noxious substances in the intestines. \n"
                               "\n"
                               "Common Side Effects: Vomiting, Constipation. \n"
                               "\n"
                               "Note: \n"
                               "\n"
                               "-Shake well before taking suspension. \n"
                               "\n"
                               "-Space 2 hours apart with any other medications. \n"
                               "\n"
                               "-Stop medication once diarrhea stops or constipations happens.\n"
                               "\n"
                               "-Stop medication and see a doctor immediately when allergy symptoms such as rash, eye swelling and difficulty in breathing occurs.")
        bot.answer_callback_query(call.id, "hi")


    elif call.data == "powder" and call.message.chat.id != currentmsgid:
        bot.send_photo(chat_id=call.message.chat.id, photo="https://imgur.com/DvjpvEN",
                       caption="We recommend using Smecta\n"
                               "Brand Name: Smecta \n"
                               "\n"
                               "Active Ingredient: Dioctahedral Smectite \n"
                               "\n"
                               "Use For: Diarrhoea \n"
                               "\n"
                               "Dosing: For children 2 to 3 sachets daily, mix with a semi-liquid food if necessary. For adults 3 sachets per day for 7 days, dilute with 50ml of water. \n"
                               "How It Works: Absorbs and remove toxins, bacteria, and noxious substances in the intestines. \n"
                               "\n"
                               "Common Side Effects: Constipation \n"
                               "\n"
                               "Note: \n"
                               "-Not suitable for patients with fructose intolerance, glucose, and galactose malabsorption syndrome, sucrase/somaltase deficiency. \n"
                               "\n"
                               "-Not recommended during pregnancy or breastfeeding. \n"
                               "\n"
                               "-Space 2 hours apart with any other medications. \n"
                               "\n"
                               "-Stop medication and see a doctor immediately when allergy symptoms such as rash, eye swelling and difficulty in breathing occurs.")
        bot.answer_callback_query(call.id, "hi")



@bot.message_handler(func=lambda call: True)
def answer(message: Message):
    if message.text == "Loperamide (Brand Name: Imodium)" \
            or message.text == "Diphenoxylate / Atropine (Brand Name: Dhamotil)" \
            or message.text == "Kaolin" \
            or message.text == "Medicinal Charcoal" \
            or message.text == "Dioctahedral Smectite (Brand Name: Smecta)":
        triedmedicineduration(message.chat.id)

    elif message.text == "Lactobacillus Acidophilus (Brand Name: Lacteol Forte)" \
            or message.text == "Oral Rehydration Salts (Brand Name: Hydralyte)" \
            or message.text == "Traditional Chinese Medicine" \
            or message.text == "No, I have not tried any diarrhoea medication yet":
        rawfood(message.chat.id)


# Diarrhoea bot
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
    mark = ReplyKeyboardMarkup(one_time_keyboard=True)
    for i in keyboard:
        mark.add(i)
    bot.send_message(text="Has the patient tried any of the diarrhoea medication below?", reply_markup=mark,
                     chat_id=message)


def howlong(message):
    keyboard = [
        [InlineKeyboardButton("More than 3 days", callback_data="serious diarrhoea")],
        [InlineKeyboardButton("Less than 3 days", callback_data="which medincine have been tried")],
    ]

    bot.send_message(text="How long has the diarrhoea lasted?", reply_markup=InlineKeyboardMarkup(keyboard),
                     chat_id=message)


def triedmedicineduration(message):
    keyboard = [
        [InlineKeyboardButton("Less than 2 days", callback_data="waitandsee")],
        [InlineKeyboardButton("More than 2 days", callback_data="serious diarrhoea")],
    ]
    bot.send_message(text="Alright.", reply_markup=ReplyKeyboardRemove(),
                     chat_id=message)
    bot.send_message(
        text="How long has the patient been taking the medication for with no improvement? (Counting from the first loose stool)",
        reply_markup=InlineKeyboardMarkup(keyboard), chat_id=message)


def rawfood(message):
    keyboard = [
        [InlineKeyboardButton("Yes", callback_data="maybe more serious condition")],
        [InlineKeyboardButton("No", callback_data="got travel")],
    ]
    bot.send_message(text="Alright.", reply_markup=ReplyKeyboardRemove(),
                     chat_id=message)
    bot.send_message(text="Has the patient eaten anything raw or undercooked recently?",
                     reply_markup=InlineKeyboardMarkup(keyboard), chat_id=message)


def diarrhoeasymptoms1(message):
    keyboard = [
        [InlineKeyboardButton("Yes", callback_data="more serious condition")],
        [InlineKeyboardButton("No", callback_data="got travel2")],
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
                          "-Symptoms of dehydration such as little or no urine, dark colored-urine, weakness, dizziness, lightheadedness, dry mouth, or skin",
                     reply_markup=InlineKeyboardMarkup(keyboard), chat_id=message)


def diarrhoeasymptoms2(message):
    keyboard = [
        [InlineKeyboardButton("Yes", callback_data="more serious condition")],
        [InlineKeyboardButton("No", callback_data="allergies")],
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
                          "-Symptoms of dehydration such as little or no urine, dark colored-urine, weakness, dizziness, lightheadedness, dry mouth, or skin",
                     reply_markup=InlineKeyboardMarkup(keyboard), chat_id=message)


def travel(message):
    keyboard = [
        [InlineKeyboardButton("Yes", callback_data="more serious condition")],
        [InlineKeyboardButton("No", callback_data="diarrhoeasymptoms2")],
    ]
    bot.send_message(text="Has the patient travelled for the past week?", reply_markup=InlineKeyboardMarkup(keyboard),
                     chat_id=message)


def travel2(message):
    keyboard = [
        [InlineKeyboardButton("Yes", callback_data="more serious condition")],
        [InlineKeyboardButton("No", callback_data="allergies")],
    ]
    bot.send_message(text="Has the patient travelled for the past week?", reply_markup=InlineKeyboardMarkup(keyboard),
                     chat_id=message)


def allergies(message):
    keyboard = [
        [InlineKeyboardButton("Yes", callback_data="have allergy")],
        [InlineKeyboardButton("No", callback_data="are you a breastfeeder")],
    ]
    bot.send_message(text="Is the patient allergic to any of the medication below?\n"
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
    bot.send_message(text="Is pregnancy or breastfeeding an issue to the patient?",
                     reply_markup=InlineKeyboardMarkup(keyboard),
                     chat_id=message)


def normaloptions(message):
    keyboard = [
        [InlineKeyboardButton("Liquid", callback_data="liquid")],
        [InlineKeyboardButton("Tablets", callback_data="tablets")],
        [InlineKeyboardButton("Capsules", callback_data="capsules")],
        [InlineKeyboardButton("Powder Sachets", callback_data="powder")],
        [InlineKeyboardButton("No Preference", callback_data="tablets")],
    ]
    bot.send_message(text="What kind of medicine will the patient prefer?", reply_markup=InlineKeyboardMarkup(keyboard),
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


# def jerod(message):
#     keyboard = [
#         [InlineKeyboardButton("Yes", callback_data="yes")],
#         [InlineKeyboardButton("No", callback_data="no")],
#     ]
#     bot.send_photo(chat_id=message, photo="https://imgur.com/a6wX2fT", caption="Do you look like this person?", reply_markup=InlineKeyboardMarkup(keyboard))
#
# def jerod2(message):
#     button1 = KeyboardButton("Send My location", request_location=True)
#     keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
#
#     keyboard.add(button1)
#
#     bot.send_message(text="We are sorry. We do not serve scum like you at our establishment. \n"
#                           "Please send us your location so that we my terminate your life promptly \n"
#                           "Alternatively, you can do the world a favor by ending your life by yourself.\n"
#                           "Have a nice day!!! \U0001F970", reply_markup=keyboard,
#                      chat_id=message)


@server.route('/' + API_KEY, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "goog", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://pharmacy-botty.herokuapp.com/' + API_KEY)
    return "good", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
