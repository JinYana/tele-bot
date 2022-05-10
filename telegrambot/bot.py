import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

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
        bot.send_message(call.message.chat.id, "This is a message")



def med(message):
    keyboard = [
        [InlineKeyboardButton("Yes", callback_data="yes"),
                InlineKeyboardButton("No", callback_data="no"),]
    ]
    bot.send_message(text="Do You Have Any Allergies?", reply_markup=InlineKeyboardMarkup(keyboard), chat_id=message)














bot.polling()
