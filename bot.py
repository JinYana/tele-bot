import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, Message, \
    ReplyKeyboardRemove
import os
from flask import Flask, request, Response

server = Flask(__name__)

API_KEY = "5324891918:AAGKD1WX7zyIlX3aLKr-GAICBjenjsH-1Mg"
bot = telebot.TeleBot(API_KEY)

person = []
panadol = []


@bot.message_handler(commands=['start'])
def start(message):
    person.clear()
    panadol.clear()
    keyboard = [
        [InlineKeyboardButton("I need help with diarrhoea!", callback_data="dia"), ],
        [InlineKeyboardButton("I need help with fever!", callback_data="fever"), ]
    ]
    bot.send_message(text="Hi what can we do for you?", reply_markup=InlineKeyboardMarkup(keyboard),
                     chat_id=message.chat.id)
    person.clear()


def triedmedicine(message):
    keyboard = [
        KeyboardButton("Loperamide (Brand Name: Imodium)"),

        KeyboardButton("Diphenoxylate / Atropine (Brand Name: Dhamotil)"),

        KeyboardButton("Kaolin (Brand Name: Kaomix)"),

        KeyboardButton("Medicinal Charcoal (Brand Name: Ultracarbon/Norit)"),

        KeyboardButton("Dioctahedral Smectite (Brand Name: Smecta)"),

        KeyboardButton("Lactobacillus Acidophilus (Brand Name: Lacteol Forte)"),

        KeyboardButton("Oral Rehydration Salts (Brand Name: Hydralyte)"),

        KeyboardButton("Traditional Chinese Medicine"),

        KeyboardButton("No, I have not tried any diarrhoea medication yet")
    ]
    mark = ReplyKeyboardMarkup(one_time_keyboard=True)
    for i in keyboard:
        mark.add(i)
    msg = bot.send_message(text="Has the patient tried any of the diarrhoea medication below?", reply_markup=mark,
                           chat_id=message.chat.id)

    bot.register_next_step_handler(msg, diamsghandler)


def diamsghandler(message):
    if message.text == "Loperamide (Brand Name: Imodium)" \
            or message.text == "Diphenoxylate / Atropine (Brand Name: Dhamotil)" \
            or message.text == "Kaolin (Brand Name: Kaomix)" \
            or message.text == "Medicinal Charcoal (Brand Name: Ultracarbon/Norit)" \
            or message.text == "Dioctahedral Smectite (Brand Name: Smecta)":
        triedmedicineduration(message.chat.id)

    elif message.text == "Lactobacillus Acidophilus (Brand Name: Lacteol Forte)" \
            or message.text == "Oral Rehydration Salts (Brand Name: Hydralyte)" \
            or message.text == "Traditional Chinese Medicine" \
            or message.text == "No, I have not tried any diarrhoea medication yet":
        rawfood(message.chat.id)


def getweight(message):
    msg = bot.send_message(text="Please type the weight of the patient in kilograms.",
                           chat_id=message.chat.id)

    bot.register_next_step_handler(msg, calculate)


def calculate(message):
    mass = int(message.text)
    if len(panadol) > 0:
        lowmass = mass * 10
        highmass = mass * 20
        bot.send_message(
            text="The estimated dosing that the patient needs are between " + lowmass + " to " + highmass + "mg.",
            chat_id=message.chat.id)
    else:
        lowmass = mass * 10
        highmass = mass * 15
        bot.send_message(
            text="The estimated dosing that the patient needs are between " + lowmass + " to " + highmass + "mg.",
            chat_id=message.chat.id)


def fevermsghandler(message):
    if message.text == "Diclofenac" \
            or message.text == "Both Paracetamol and Ibuprofen" \
            or message.text == "Ibuprofen":
        panadol.clear()

        feverimproved(message.chat.id, False)

    elif message.text == "Paracetamol":
        panadol.clear()
        feverimproved(message.chat.id, True)
        panadol.append("yes")


    elif message.text == "Traditional Chinese Medicine" \
            or message.text == "No, I have not tried any fever medication yet":
        panadol.clear()

        feverallergy(message.chat.id, False)


def feverallergy(message, paracetamol):
    if paracetamol:
        keyboard = [
            KeyboardButton("Ibuprofen"),

            KeyboardButton("Any other non-steroidal anti-inflammatory drugs (NSAIDs)"),

            KeyboardButton("No allergies to the medications listed"),

        ]
        mark = ReplyKeyboardMarkup(one_time_keyboard=True)
        for i in keyboard:
            mark.add(i)
        msg = bot.send_message(text="Is the patient allergic to any of the medication?", reply_markup=mark,
                               chat_id=message)
        bot.register_next_step_handler(msg, feverallergymsghandler, paracetamol=True)


    else:
        keyboard = [
            KeyboardButton("Ibuprofen"),

            KeyboardButton("Paracetamol"),

            KeyboardButton("Ibuprofen AND Paracetamol"),

            KeyboardButton("Any other non-steroidal anti-inflammatory drugs (NSAIDs)"),

            KeyboardButton("No allergies to the medications listed"),

        ]
        mark = ReplyKeyboardMarkup(one_time_keyboard=True)
        for i in keyboard:
            mark.add(i)
        msg = bot.send_message(text="Is the patient allergic to any of the medication?", reply_markup=mark,
                               chat_id=message)
        bot.register_next_step_handler(msg, feverallergymsghandler, paracetamol=False)




def feverallergymsghandler(message, paracetamol):

    if (message.text == "Ibuprofen" and paracetamol and person[0] == "a") \
            or (message.text == "Any other non-steroidal anti-inflammatory drugs (NSAIDs)" and paracetamol and person[
        0] == "a") \
            or (message.text == "Ibuprofen AND Paracetamol" and not paracetamol and person[0] == "a"):
        bot.send_message(text="Alright.", reply_markup=ReplyKeyboardRemove(),
                         chat_id=message.chat.id)
        bot.send_message(text="Oh no! It seems like both over-the-counter fever medications won’t work for you. "
                              "Be kindly advised to seek treatment from a doctor or a healthcare professional "
                              "as soon as possible. Get well soon! \n"
                              "\n"
                              "In the meantime, what the patient can do are: \n"
                              "\n"
                              "-Drink plenty of fluids \n"
                              "\n"
                              "-Avoid caffeine of any form \n"
                              "\n"
                              "-Take plenty of rest \n"
                              "\n"
                              "-Place cool tower to the skin near the neck and to the armpits \n",
                         chat_id=message.chat.id)

    elif (message.text == "Ibuprofen" and paracetamol and person[0] == "c") \
            or (message.text == "Any other non-steroidal anti-inflammatory drugs (NSAIDs)" and paracetamol and person[
        0] == "c") \
            or (message.text == "Ibuprofen AND Paracetamol" and not paracetamol and person[0] == "c"):
        bot.send_message(text="Alright.", reply_markup=ReplyKeyboardRemove(),
                         chat_id=message.chat.id)
        bot.send_message(text="Oh no! It seems like both over-the-counter fever medications won’t work for you. "
                              "Be kindly advised to seek treatment from a doctor or a healthcare professional "
                              "as soon as possible. Get well soon! \n"
                              "\n"
                              "In the meantime, what the patient can do are: \n"
                              "\n"
                              "-Drink plenty of fluids \n"
                              "\n"
                              "-Take plenty of rest \n"
                              "\n"
                              "-Make sure the child’s environment is not too hot and is comfortable \n"
                              "\n"
                              "-Dress child in light clothing \n"
                              "\n"
                              "-Sponge with room temperature water to the skin near the neck and to the armpits \n",
                         chat_id=message.chat.id)


    elif (message.text == "Ibuprofen" and not paracetamol) \
            or (message.text == "Any other non-steroidal anti-inflammatory drugs (NSAIDs)" and not paracetamol) \
            or message.text == "Paracetamol" or message.text == "No allergies to the medications listed":
        dengue(message.chat.id)

def dengue(message):

    if len(panadol) > 0:
        keyboard = [
            [InlineKeyboardButton("Yes", callback_data="got dengue")],
            [InlineKeyboardButton("No", callback_data="no dengue")],
        ]
    else:
        keyboard = [
            [InlineKeyboardButton("Yes", callback_data="no dengue")],
            [InlineKeyboardButton("No", callback_data="no dengue")],
        ]

    bot.send_message(text="Alright.", reply_markup=ReplyKeyboardRemove(),
                     chat_id=message)


    bot.send_message(
        text="Is your fever associated with Dengue or Chicken Pox? \n"
             " \n"
             " \n"
             "Symptoms for Dengue: \n"
             " \n"
             "-Sudden fever lasting 2 to 7 days \n"
             " \n"
             "-Pain behind eyes with severe headache \n"
             " \n"
             "-Muscle and joint pain-Skin rashes \n"
             " \n"
             "-Nausea and vomiting \n"
             " \n"
             "-Mild bleeding such as nose or gum bleed and easily bruising of skin \n"
             " \n"
             " \n"
             "Symptoms of Chicken Pox: \n"
             " \n"
             "-Fever \n"
             " \n"
             "-Itchy red spots on body and face that turns to blister progressively, which will burst, dry up, and form crusts \n",
        reply_markup=InlineKeyboardMarkup(keyboard), chat_id=message)

def prego(message):
    if panadol[0] == "yes":
        keyboard = [
            [InlineKeyboardButton("Yes", callback_data="got prego")],
            [InlineKeyboardButton("No", callback_data="no dengue")],
        ]
    else:
        keyboard = [
            [InlineKeyboardButton("Yes", callback_data="no prego")],
            [InlineKeyboardButton("No", callback_data="no prego")],
        ]

    bot.send_message(
        text="Is pregnancy an issue to the patient?",
        reply_markup=InlineKeyboardMarkup(keyboard), chat_id=message)

def feverprefer(message):
    if len(panadol) > 0:
        keyboard = [
            [InlineKeyboardButton("Liquid", callback_data="got prego")],
            [InlineKeyboardButton("Tablets", callback_data="no dengue")],
        ]
    else:
        if person[0] == "c":
            keyboard = [
                [InlineKeyboardButton("Liquid", callback_data="fever liquid child")],
                [InlineKeyboardButton("Suppository", callback_data="fever suppository child")],
                [InlineKeyboardButton("Chewable Tablets", callback_data="fever chewable child")],
            ]
        else:
            keyboard = [
                [InlineKeyboardButton("Liquid", callback_data="fever liquid adult")],
                [InlineKeyboardButton("Suppository", callback_data="fever suppository adult")],
                [InlineKeyboardButton("Tablets", callback_data="fever tablets adult")],
            ]

    bot.send_message(
        text="What will the patient prefer?",
        reply_markup=InlineKeyboardMarkup(keyboard), chat_id=message)



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


def ages(message, condition):
    if condition == "diarrhoea":
        keyboard = [

            [InlineKeyboardButton("Infant (0-1 Y.O.)", callback_data="unsuitable age")],

            [InlineKeyboardButton("Elderly (65 Y.O. and above)", callback_data="unsuitable age")],

            [InlineKeyboardButton("Children (2-17 Y.O.)", callback_data="how long diarrhoea")],

            [InlineKeyboardButton("Adult (18-64 Y.O.)", callback_data="how long diarrhoea")],

        ]
    else:
        keyboard = [

            [InlineKeyboardButton("Infant (0-1 Y.O.)", callback_data="fever unsuitable age")],

            [InlineKeyboardButton("Children (6 Mnth-12 Y.O.)", callback_data="how long fever child")],

            [InlineKeyboardButton("Adult (13 Y.O. and above)", callback_data="how long fever adult")],

        ]

    bot.send_message(text="How old is the patient?", reply_markup=InlineKeyboardMarkup(keyboard), chat_id=message)


def howlong(message, condition, age):
    if condition == "diarrhoea":
        keyboard = [
            [InlineKeyboardButton("More than 3 days", callback_data="serious diarrhoea")],
            [InlineKeyboardButton("Less than 3 days", callback_data="which medincine have been tried")],
        ]
        bot.send_message(text="How long has the diarrhoea lasted?", reply_markup=InlineKeyboardMarkup(keyboard),
                         chat_id=message)
    else:
        if age == "c":
            keyboard = [
                [InlineKeyboardButton("More than 3 days", callback_data="serious fever")],
                [InlineKeyboardButton("Less than 3 days", callback_data="fever symptoms child")],
            ]
        else:
            keyboard = [
                [InlineKeyboardButton("More than 3 days", callback_data="serious fever")],
                [InlineKeyboardButton("Less than 3 days", callback_data="fever symptoms adult")],
            ]

        bot.send_message(text="How long has the fever lasted?", reply_markup=InlineKeyboardMarkup(keyboard),
                         chat_id=message)


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


def feversymptoms(message, age):
    keyboard = [
        [InlineKeyboardButton("Yes", callback_data="yes fever symptoms")],
        [InlineKeyboardButton("No", callback_data="no fever symptoms")],
    ]
    if age == "c":

        bot.send_message(text="Has the patient developed any of the symptoms below? \n"
                              "\n"
                              "-Temperature is higher than 40°C \n"
                              "\n"
                              "-Red or purple rashes developing \n"
                              "\n"
                              "-Headache, stiff neck or is discomfort under bright light \n"
                              "\n"
                              "-Difficulty in breathing, faints or not responding \n"
                              "\n"
                              "-Has a fit or lacks energy \n"
                              "\n"
                              "-Look more unwell \n"
                              "\n"
                              "-Display symptoms of dehydration such as sunken eyes, dry diapers, and poor elasticity",
                         reply_markup=InlineKeyboardMarkup(keyboard),
                         chat_id=message)
    else:

        bot.send_message(text="Has the patient displayed any of the symptoms below? \n"
                              "\n"
                              "-Temperature is or higher than 39.4°C-Symptoms worsen \n"
                              "\n"
                              "-Feeling confused or stiff neck-Skin rashes developing \n"
                              "\n"
                              "-Very bad diarrhoea, headache or vomiting occurs \n"
                              "\n"
                              "-Difficulty in breathing or chest pain \n"
                              "\n"
                              "-If patient have cancer, heart diseases, diabetes, AIDS or are taking medicines "
                              "that might weaken the immune system",
                         reply_markup=InlineKeyboardMarkup(keyboard),
                         chat_id=message)


def triedfevermedicine(message):
    keyboard = [
        KeyboardButton("Diclofenac"),

        KeyboardButton("Both Paracetamol and Ibuprofen"),

        KeyboardButton("Ibuprofen"),

        KeyboardButton("Paracetamol"),

        KeyboardButton("Traditional Chinese Medicine"),

        KeyboardButton("No, I have not tried any fever medication yet"),

    ]
    mark = ReplyKeyboardMarkup(one_time_keyboard=True)
    for i in keyboard:
        mark.add(i)
    msg = bot.send_message(text="Has the patient tried any of the fever medication below?", reply_markup=mark,
                           chat_id=message)

    bot.register_next_step_handler(msg, fevermsghandler)


def feverimproved(message, paracetamol):
    if paracetamol:
        keyboard = [
            [InlineKeyboardButton("Yes", callback_data="yes fever improve")],
            [InlineKeyboardButton("No", callback_data="no paracetamol fever never improve")],
        ]

    else:
        keyboard = [
            [InlineKeyboardButton("Yes", callback_data="yes fever improve")],
            [InlineKeyboardButton("No", callback_data="no fever never improve")],
        ]

    bot.send_message(text="Alright.", reply_markup=ReplyKeyboardRemove(),
                     chat_id=message)

    bot.send_message(text="Has the medication improved the patient’s fever?",
                     reply_markup=InlineKeyboardMarkup(keyboard),
                     chat_id=message)







@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "dia":
        ages(call.message.chat.id, "diarrhoea")
        bot.answer_callback_query(call.id, "")

    elif call.data == "fever":
        ages(call.message.chat.id, "fever")
        bot.answer_callback_query(call.id, "")

    # elif call.data == "yes":
    #     jerod2(call.message.chat.id)
    #
    # elif call.data == "no":
    #     age(call.message.chat.id)

    elif call.data == "unsuitable age":
        bot.send_message(call.message.chat.id,
                         "Oh no! Due to the age, patient is at high risk of developing complications due to diarrhoea. Be kindly advised to seek treatment from a doctor or a healthcare professional as soon as possible. Get well soon!")
        bot.answer_callback_query(call.id, "")

    elif call.data == "how long diarrhoea":
        howlong(call.message.chat.id, "diarrhoea", " ")
        bot.answer_callback_query(call.id, "")

    elif call.data == "serious diarrhoea":
        bot.send_message(call.message.chat.id,
                         "Oh no! The diarrhoea seems to be much more serious than expected. Be kindly advised to seek "
                         "treatment from a doctor or a healthcare professional as soon as possible. Get well soon!")
        bot.answer_callback_query(call.id, "")



    elif call.data == "which medincine have been tried":
        triedmedicine(call.message)


    elif call.data == "waitandsee":
        bot.send_message(call.message.chat.id,
                         "You might want to continue the medication for 2 days from the first loose stool to see if "
                         "there is any improvement. If there is still no improvement after 2 days, seek treatment from "
                         "a doctor or healthcare professional as soon as possible. Get well soon")
        bot.answer_callback_query(call.id, "")


    elif call.data == "maybe more serious condition":
        diarrhoeasymptoms1(call.message.chat.id)
        bot.answer_callback_query(call.id, "")

    elif call.data == "diarrhoeasymptoms2":
        diarrhoeasymptoms2(call.message.chat.id)
        bot.answer_callback_query(call.id, "")

    elif call.data == "more serious condition":
        bot.send_message(call.message.chat.id,
                         "Oh no! The symptoms might be a sign of a more serious condition. Be kindly advised to seek "
                         "treatment from a doctor or a healthcare professional as soon as possible. Get well soon")
        bot.answer_callback_query(call.id, "")


    elif call.data == "got travel":
        travel(call.message.chat.id)
        bot.answer_callback_query(call.id, "")

    elif call.data == "got travel2":
        travel2(call.message.chat.id)
        bot.answer_callback_query(call.id, "")

    elif call.data == "allergies":
        allergies(call.message.chat.id)
        bot.answer_callback_query(call.id, "")

    elif call.data == "have allergy":
        bot.send_message(call.message.chat.id,
                         "Oh no! You might want to seek treatment from a doctor or healthcare professional as soon "
                         "as possible to prevent triggering any of the allergies from the medications. Get well soon!")
        bot.answer_callback_query(call.id, "")

    elif call.data == "are you a breastfeeder":
        breastfeed(call.message.chat.id)
        bot.answer_callback_query(call.id, "")

    elif call.data == "pregnant options":
        pregnantoptions(call.message.chat.id)
        bot.answer_callback_query(call.id, "")

    elif call.data == "normal options":
        normaloptions(call.message.chat.id)
        bot.answer_callback_query(call.id, "")

    elif call.data == "tablets":
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

        bot.answer_callback_query(call.id, "")



    elif call.data == "capsules":
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
        bot.answer_callback_query(call.id, "")


    elif call.data == "liquid":
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
        bot.answer_callback_query(call.id, "")


    elif call.data == "powder":
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
        bot.answer_callback_query(call.id, "")




    elif call.data == "fever unsuitable age":
        bot.send_message(call.message.chat.id,
                         "Oh no! Due to the age, patient is at high risk of developing complications from fever. "
                         "Be kindly advised to seek treatment from a doctor or a healthcare professional as soon "
                         "as possible. Get well soon!")
        bot.answer_callback_query(call.id, "")

    elif call.data == "how long fever child":
        person.clear()
        howlong(call.message.chat.id, "fever", 'c')
        person.append("c")
        bot.answer_callback_query(call.id, "")

    elif call.data == "how long fever adult":
        person.clear()
        howlong(call.message.chat.id, "fever", "a")
        person.append("a")
        bot.answer_callback_query(call.id, "")

    elif call.data == "fever symptoms child":
        feversymptoms(call.message.chat.id, "c")
        bot.answer_callback_query(call.id, "")

    elif call.data == "fever symptoms adult":
        feversymptoms(call.message.chat.id, "a")
        bot.answer_callback_query(call.id, "")

    elif call.data == "yes fever symptoms":
        bot.send_message(call.message.chat.id,
                         "Oh no! The symptoms might be a sign of a more serious condition. "
                         "Be kindly advised to seek treatment from a doctor or a healthcare professional "
                         "as soon as possible. Get well soon!")
        bot.answer_callback_query(call.id, "")

    elif call.data == "no fever symptoms":
        triedfevermedicine(call.message.chat.id)
        bot.answer_callback_query(call.id, "")

    elif call.data == "no fever never improve":
        bot.send_message(call.message.chat.id,
                         "Oh no! The fever seems to be much more serious than expected. Be kindly advised to seek "
                         "treatment from a doctor or a healthcare professional as soon as possible. Get well soon!")
        bot.answer_callback_query(call.id, "")

    elif call.data == "yes fever improve":
        bot.send_message(call.message.chat.id,
                         "Patient might want to continue the same treatment until recovery or if there is no resolution,"
                         " seek treatment from a doctor or healthcare professional as soon as possible. Get well soon!")
        bot.answer_callback_query(call.id, "")

    elif call.data == "no paracetamol fever never improve":
        feverallergy(call.message.chat.id, True)
        bot.answer_callback_query(call.id, "")

    elif call.data == "got dengue":
        if person[0] == "a":
            bot.send_message(call.message.chat.id,
                             "Oh no! It seems like both over-the-counter fever medications won’t work for you. "
                             "Be kindly advised to seek treatment from a doctor or a healthcare professional "
                             "as soon as possible. Get well soon! \n"
                             "\n"
                             "In the meantime, what the patient can do are: \n"
                             "\n"
                             "-Drink plenty of fluids \n"
                             "\n"
                             "-Avoid caffeine of any form \n"
                             "\n"
                             "-Take plenty of rest \n"
                             "\n"
                             "-Place cool tower to the skin near the neck and to the armpits \n", )
            bot.answer_callback_query(call.id, "")
        else:
            bot.send_message(call.message.chat.id, "Oh no! It seems like both over-the-counter fever medications won’t work for you. "
                                  "Be kindly advised to seek treatment from a doctor or a healthcare professional "
                                  "as soon as possible. Get well soon! \n"
                                  "\n"
                                  "In the meantime, what the patient can do are: \n"
                                  "\n"
                                  "-Drink plenty of fluids \n"
                                  "\n"
                                  "-Take plenty of rest \n"
                                  "\n"
                                  "-Make sure the child’s environment is not too hot and is comfortable \n"
                                  "\n"
                                  "-Dress child in light clothing \n"
                                  "\n"
                                  "-Sponge with room temperature water to the skin near the neck and to the armpits \n")
            bot.answer_callback_query(call.id, "")

    elif call.data == "no dengue":
        if person[0] == "a":
            prego(call.message.chat.id)
            bot.answer_callback_query(call.id, "")
        else:
            if len(panadol) > 0:

                bot.send_photo(chat_id=call.message.chat.id, photo="https://imgur.com/DvjpvEN",
                               caption="Brand Name: Brufen \n"
                                       " \n"
                                       "Active Ingredient: Ibuprofen \n"
                                       " \n"
                                       "Use For: Fever and Pain relieve. \n"
                                       " \n"
                                       "Dosing: 5-10mg/kg of child’s body weight \n"
                                       " \n"
                                       "How It Works: Exhibits analgesic, antipyretic, and anti-inflammatory effects. \n"
                                       " \n"
                                       "Common Side Effects: diarrhea, constipation, nausea, stomach pain, bloating, and photosensitivity. \n"
                                       " \n"
                                       " \n"
                                       "Note:  \n"
                                       " \n"
                                       "-Do not take if you have severe heart, liver, or kidney failure. \n"
                                       " \n"
                                       "-Do not take if you have stomach bleeding, perforation, or ulcers. \n"
                                       " \n"
                                       "-Do not take if you are pregnant or have increased risk of bleeding. \n"
                                       " \n"
                                       "-Do not take if you are allergic to any other non-steroidal anti-inflammatory drugs (NSAIDs). \n"
                                       " \n"
                                       "-Do not take if you have worsening or severe asthma. \n"
                                       " \n"
                                       "-Stop medication and see a doctor immediately when allergy symptoms such as rash, eye swelling and difficulty in breathing occurs")

                keyboard = [
                    [InlineKeyboardButton("Yes", callback_data="calculate")],
                    [InlineKeyboardButton("No", callback_data="dont calculate")],
                ]

                bot.send_message(text="Do you need help calculating the dosage for the patient?", reply_markup=InlineKeyboardMarkup(keyboard),
                                 chat_id=call.message.chat.id)
            else:
                feverprefer(call.message.chat.id)


    elif call.data == "got prego":
        bot.send_message(call.message.chat.id,
                         "Oh no! It seems like both over-the-counter fever medications won’t work for you. "
                         "Be kindly advised to seek treatment from a doctor or a healthcare professional "
                         "as soon as possible. Get well soon! \n"
                         "\n"
                         "In the meantime, what the patient can do are: \n"
                         "\n"
                         "-Drink plenty of fluids \n"
                         "\n"
                         "-Avoid caffeine of any form \n"
                         "\n"
                         "-Take plenty of rest \n"
                         "\n"
                         "-Place cool tower to the skin near the neck and to the armpits \n")
        bot.answer_callback_query(call.id, "")

    elif call.data == "no prego":
        if len(panadol) > 0:
            bot.send_photo(chat_id=call.message.chat.id, photo="https://imgur.com/DvjpvEN",
                           caption="Brand Name: Neurofen \n"
                                   " \n"
                                   "Active Ingredient: Ibuprofen \n"
                                   " \n"
                                   "Use For: Fever and Pain relieve. \n"
                                   " \n"
                                   "Dosing: 1-2 tablets, 3 times a day. \n"
                                   " \n"
                                   "How It Works: Exhibits analgesic, antipyretic, and anti-inflammatory effects. \n"
                                   " \n"
                                   "Common Side Effects: diarrhea, constipation, nausea, stomach pain, bloating, and photosensitivity. \n"
                                   " \n"
                                   " \n"
                                   "Note:  \n"
                                   " \n"
                                   "-Do not take if you have severe heart, liver, or kidney failure. \n"
                                   " \n"
                                   "-Do not take if you have stomach bleeding, perforation, or ulcers. \n"
                                   " \n"
                                   "-Do not take if you are pregnant or have increased risk of bleeding. \n"
                                   " \n"
                                   "-Do not take if you are allergic to any other non-steroidal anti-inflammatory drugs (NSAIDs). \n"
                                   " \n"
                                   "-Do not take if you have worsening or severe asthma. \n"
                                   " \n"
                                   "-Stop medication and see a doctor immediately when allergy symptoms such as rash, eye swelling and difficulty in breathing occurs")

            bot.answer_callback_query(call.id, "")


        else:
            feverprefer(call.message.chat.id)

    elif call.data == "fever liquid child":
        bot.send_photo(chat_id=call.message.chat.id, photo="https://imgur.com/DvjpvEN",
                       caption="Brand Name: Panadol Children Suspension \n"
                         " \n"
                         "Active Ingredient: Paracetamol \n"
                         " \n"
                         "Use For: Fever and Pain relieve. \n"
                         " \n"
                         "Dosing: 10-15mg/kg of child’s body weight (Refer to leaflet). \n"
                         " \n"
                         "How It Works: Exhibits analgesic, antipyretic, and weak anti-inflammatory effects. \n"
                         " \n"
                         "Common Side Effects: Hematological reactions\n"
                         " \n"
                         " \n"
                         "Note: \n"
                         " \n"
                         "-Avoid taking with blood thinner medications. \n"
                         " \n"
                         "-Do not take more than 4 doses in any 24H period. \n"
                         " \n"
                         "-Do not take more frequently than 4H. \n"
                         " \n"
                         "-Do not take for more than 3 days unless told so. \n"
                         " \n"
                         "-If fever persists for more than 24H (4 doses), please seek medical attention as soon as possible. \n"
                         " \n"
                         "-Stop medication and see a doctor immediately when allergy symptoms such as rash, eye "
                         " \n"
                         "swelling and difficulty in breathing occurs.")

        keyboard = [
            [InlineKeyboardButton("Yes", callback_data="calculate")],
            [InlineKeyboardButton("No", callback_data="dont calculate")],
        ]

        bot.send_message(text="Do you need help calculating the dosage for the patient?",
                         reply_markup=InlineKeyboardMarkup(keyboard),
                         chat_id=call.message.chat.id)


    elif call.data == "fever chewable child":
        bot.send_photo(chat_id=call.message.chat.id, photo="https://imgur.com/DvjpvEN",
                       caption="Brand Name: Panadol for Children Chewable Tablets \n"
                         " \n"
                         "Active Ingredient: Paracetamol \n"
                         " \n"
                         "Use For: Fever and Pain relieve. \n"
                         " \n"
                         "Dosing: 10-15mg/kg of child’s body weight (Refer to leaflet). \n"
                         " \n"
                         "How It Works: Exhibits analgesic, antipyretic, and weak anti-inflammatory effects. \n"
                         " \n"
                         "Common Side Effects: Hematological reactions \n"
                         " \n"
                         " \n"
                         "Note:  \n"
                         " \n"
                         "-Avoid taking with blood thinner medications. \n"
                         " \n"
                         "-Do not take more than 4 doses in any 24H period. \n"
                         " \n"
                         "-Do not take more frequently than 4H.-Do not take for more than 3 days unless told so. \n"
                         " \n"
                         "-If fever persists for more than 24H (4 doses), please seek medical attention as soon as possible. \n"
                         " \n"
                         "-Stop medication and see a doctor immediately when allergy symptoms such as rash, eye swelling and difficulty in breathing occurs.")

        keyboard = [
            [InlineKeyboardButton("Yes", callback_data="calculate")],
            [InlineKeyboardButton("No", callback_data="dont calculate")],
        ]

        bot.send_message(text="Do you need help calculating the dosage for the patient?",
                         reply_markup=InlineKeyboardMarkup(keyboard),
                         chat_id=call.message.chat.id)


    elif call.data == "fever suppository child":
        bot.send_photo(chat_id=call.message.chat.id, photo="https://imgur.com/DvjpvEN",
                       caption="Brand Name: Remedol 125 Suppository  \n"
                         " \n"
                         "Active Ingredient: Paracetamol \n"
                         " \n"
                         "Use For: Fever and Pain relieve. \n"
                         " \n"
                         "Dosing: 1-6 Y.O. (1 suppository of 250mg), 6-12Y.O. (1 suppository of 500mg) \n"
                         " \n"
                         "How It Works: Exhibits analgesic, antipyretic, and weak anti-inflammatory effects. \n"
                         " \n"
                         "Common Side Effects: Hematological reactions, Skin rashes. \n"
                         " \n"
                         "Note: \n"
                         " \n"
                         "-Avoid taking with blood thinner medications. \n"
                         " \n"
                         "-Do not take more than 4 doses in any 24H period. \n"
                         " \n"
                         "-Do not take more frequently than 4H.-Do not take for more than 3 days unless told so. \n"
                         " \n"
                         "-If fever persists for more than 24H (4 doses), please seek medical attention as soon as possible. \n"
                         " \n"
                         "-Stop medication and see a doctor immediately when allergy symptoms such as rash, eye swelling and difficulty in breathing occurs.")

        keyboard = [
            [InlineKeyboardButton("Yes", callback_data="calculate")],
            [InlineKeyboardButton("No", callback_data="dont calculate")],
        ]

        bot.send_message(text="Do you need help calculating the dosage for the patient?",
                         reply_markup=InlineKeyboardMarkup(keyboard),
                         chat_id=call.message.chat.id)

    elif call.data == "fever liquid adult":
        bot.send_photo(chat_id=call.message.chat.id, photo="https://imgur.com/DvjpvEN",
                       caption="Brand Name: Paximol 500 Oral Mixture \n"
                               " \n"
                               "Active Ingredient: Paracetamol \n"
                               " \n"
                               "Use For: Fever and Pain relieve. \n"
                               " \n"
                               "Dosing: one to two 5ml spoonful (500mg) 3-4 times a day. \n"
                               " \n"
                               "How It Works: Exhibits analgesic, antipyretic, and weak anti-inflammatory effects. \n"
                               " \n"
                               "Common Side Effects: Hematological reactions \n"
                               " \n"
                               " \n"
                               "Note:  \n"
                               " \n"
                               "-Avoid taking with blood thinner medications. \n"
                               " \n"
                               "-Do not take more than 4 doses in any 24H period. \n"
                               " \n"
                               "-Do not take more frequently than 4H. \n"
                               " \n"
                               "-Do not take for more than 3 days unless told so. \n"
                               " \n"
                               "-If fever persists for more than 24H (4 doses), please seek medical attention as soon as possible. \n"
                               " \n"
                               "-Stop medication and see a doctor immediately when allergy symptoms such as rash, eye swelling and difficulty in breathing occurs. \n")

        bot.answer_callback_query(call.id, "")

    elif call.data == "fever suppository adult":
        bot.send_photo(chat_id=call.message.chat.id, photo="https://imgur.com/DvjpvEN",
                       caption="Brand Name: Poro Suppository 250 \n"
                               " \n"
                               "Active Ingredient: Paracetamol \n"
                               " \n"
                               "Use For: Fever and Pain relieve. \n"
                               " \n"
                               "Dosing: 2-3 suppository, every 3-4 times a week \n"
                               " \n"
                               "How It Works: Exhibits analgesic, antipyretic, and weak anti-inflammatory effects. \n"
                               " \n"
                               "Common Side Effects: Hematological reactions \n"
                               " \n"
                               " \n"
                               "Note:  \n"
                               " \n"
                               "-Avoid taking with blood thinner medications. \n"
                               " \n"
                               "-Do not take more than 4 doses in any 24H period. \n"
                               " \n"
                               "-Do not take more frequently than 4H. \n"
                               " \n"
                               "-Do not take for more than 3 days unless told so. \n"
                               " \n"
                               "-If fever persists for more than 24H (4 doses), please seek medical attention as soon as possible. \n"
                               " \n"
                               "-Stop medication and see a doctor immediately when allergy symptoms such as rash, eye swelling and difficulty in breathing occurs. \n")

        bot.answer_callback_query(call.id, "")

    elif call.data == "fever tablet adult":
        bot.send_photo(chat_id=call.message.chat.id, photo="https://imgur.com/DvjpvEN",
                       caption="Brand Name: Tylenol \n"
                               " \n"
                               "Active Ingredient: Paracetamol \n"
                               " \n"
                               "Use For: Fever and Pain relieve. \n"
                               " \n"
                               "Dosing: 1-2 tablets every 4-6 hours \n"
                               " \n"
                               "How It Works: Exhibits analgesic, antipyretic, and weak anti-inflammatory effects. \n"
                               " \n"
                               "Common Side Effects: Hematological reactions \n"
                               " \n"
                               " \n"
                               "Note:  \n"
                               " \n"
                               "-Avoid taking with blood thinner medications. \n"
                               " \n"
                               "-Do not take more than 4 doses in any 24H period. \n"
                               " \n"
                               "-Do not take more frequently than 4H. \n"
                               " \n"
                               "-Do not take for more than 3 days unless told so. \n"
                               " \n"
                               "-If fever persists for more than 24H (4 doses), please seek medical attention as soon as possible. \n"
                               " \n"
                               "-Stop medication and see a doctor immediately when allergy symptoms such as rash, eye swelling and difficulty in breathing occurs. \n")

        bot.answer_callback_query(call.id, "")

    elif call.data == "calculate":
        getweight(call.message.chat.id)








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
