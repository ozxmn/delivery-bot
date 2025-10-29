import telebot
from telebot import types
import urllib.request
import json
import time
import logging

logging.basicConfig(level=logging.INFO)

bot = telebot.TeleBot("YOUR_BOT_TOKEN")
user_languages = {}
user_messages = {}
confirmation_messages = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("Қазақ", callback_data="qz")
    item2 = types.InlineKeyboardButton("English", callback_data="en")
    markup.add(item1, item2)
    bot.send_message(message.chat.id, "Тілді таңдаңыз / Choose language", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ['qz', 'en'])
def lang_query(call):
    if call.data == 'qz':
        user_languages[call.from_user.id] = 0
    elif call.data == 'en':
        user_languages[call.from_user.id] = 1
    lang = user_languages[call.from_user.id]
    bot.send_message(call.message.chat.id,
                     "Курьер жеткізу адресің білу үшін мекен-жайыңызды жіберіңіз" if lang == 0
                     else "Send your location so the courier knows your delivery address",
                     reply_markup=create_location_keyboard(lang))

def create_location_keyboard(lang):
    text_kazakh = "Мекен-жайымды жіберу"
    text_english = "Send my location"
    item1 = types.KeyboardButton(text_kazakh if lang == 0 else text_english, request_location=True)
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    markup.add(item1)
    return markup

@bot.callback_query_handler(func=lambda call: call.data in ['yes', 'no'])
def callback_query(call):
    lang = user_languages.get(call.from_user.id, 0)
    if call.data == "yes":
        markup = types.InlineKeyboardMarkup(row_width=1)
        item1 = types.InlineKeyboardButton(text="🌯🥤 Menu 🍔🥪", web_app=types.WebAppInfo(
        url="https://yesdelivery-nu.vercel.app" if lang == 0 else "https://yesdelivery-nu.vercel.app/menu_en.html"))
        item2 = types.InlineKeyboardButton(
        "Мекенжайды өзгерту📍" if lang == 0 else "Change location📍", callback_data='change_location')
        item3 = types.InlineKeyboardButton("Тіл / Язык", callback_data='change_language')
        markup.add(item1, item2, item3)
        sent_message = bot.edit_message_text("Төмендегілердің бірін таңдаңыз" if lang == 0 else "Choose one of the following",
                                             call.message.chat.id,confirmation_messages.pop(call.from_user.id), reply_markup=markup)
        user_messages[call.message.chat.id] = sent_message.message_id
    elif call.data == "no":
        bot.delete_message(call.message.chat.id, confirmation_messages.pop(call.from_user.id))
        text_kazakh = "Мекен-жайымды жіберу"
        text_english = "Send my location"
        item1 = types.KeyboardButton(text_kazakh if lang == 0 else text_english, request_location=True)
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        markup.add(item1)
        bot.send_message(call.message.chat.id,
                         "Курьер жеткізу адресің білу үшін мекен-жайыңызды жіберіңіз" if lang == 0
                         else "Send your location so the courier knows your delivery address",
                         reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ['change_location', 'change_language'])
def change_query(call):
    lang = user_languages.get(call.from_user.id, 0)
    if call.data == "change_location":
        text_kazakh = "Мекен-жайымды жіберу"
        text_english = "Send my location"
        item1 = types.KeyboardButton(text_kazakh if lang == 0 else text_english, request_location=True)
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        markup.add(item1)
        bot.send_message(call.message.chat.id,
                         "Курьер жеткізу адресің білу үшін мекен-жайыңызды жіберіңіз" if lang == 0
                         else "Send your location so the courier knows your delivery address",
                         reply_markup=markup)
    elif call.data == "change_language":
        if call.from_user.id not in user_languages:
            user_languages[call.from_user.id] = 0
        user_languages[call.from_user.id] = 1 - user_languages[call.from_user.id]
        lang = user_languages[call.from_user.id]
        if call.from_user.id in user_messages:
            msg_id = user_messages[call.from_user.id]
            markup = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton(text="🌯🥤 Menu 🍔🥪", web_app=types.WebAppInfo(
                url="https://yesdelivery-nu.vercel.app" if lang == 0 else "https://yesdelivery-nu.vercel.app/menu_en.html"))
            item2 = types.InlineKeyboardButton(
                "Мекенжайды өзгерту📍" if lang == 0 else "Change location📍", callback_data='change_location')
            item3 = types.InlineKeyboardButton("Тіл / Язык", callback_data='change_language')
            markup.add(item1)
            markup.add(item2)
            markup.add(item3)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=msg_id,
                                  text="Төмендегілердің бірін таңдаңыз" if lang == 0 else "Choose one of the following",
                                  reply_markup=markup)

@bot.message_handler(content_types=['location'])
def handle_location(message):
    lang = user_languages.get(message.from_user.id, 0)
    latitude = message.location.latitude
    longitude = message.location.longitude
    link = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}&zoom=18&addressdetails=0&accept-language=kk-KZ"
    with urllib.request.urlopen(link) as url:
        data = json.load(url)
    confirmation_text = "Осы мекенжай дұрыс па?: " + data['display_name'] if lang == 0 else f"Is this your location?: {data['display_name']}"
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton("Иә ✅" if lang == 0 else "Yes ✅", callback_data='yes')
    item2 = types.InlineKeyboardButton("Жоқ ⛔" if lang == 0 else "No ⛔", callback_data='no')
    markup.add(item1, item2)
    processing_message = bot.send_message(message.chat.id, '♻️Processing your request♻️', reply_markup=types.ReplyKeyboardRemove())
    bot.delete_message(chat_id=message.chat.id, message_id=processing_message.message_id)
    confirmation_message = bot.send_message(message.chat.id, confirmation_text, reply_markup=markup)
    confirmation_messages[message.from_user.id] = confirmation_message.message_id

def send_function_options(chat_id, lang):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton(text="🌯🥤 Menu 🍔🥪", web_app=types.WebAppInfo(
        url="https://yesdelivery-nu.vercel.app" if lang == 0 else "https://yesdelivery-nu.vercel.app/menu_en.html"))
    item2 = types.InlineKeyboardButton(
        "Мекенжайды өзгерту📍" if lang == 0 else "Change location📍", callback_data='change_location')
    item3 = types.InlineKeyboardButton("Тіл / Язык", callback_data='change_language')
    markup.add(item1, item2, item3)
    sent_message = bot.send_message(chat_id,
                                    "Төмендегілердің бірін таңдаңыз" if lang == 0 else "Choose one of the following",
                                    reply_markup=markup)
    user_messages[chat_id] = sent_message.message_id

while True:
    try:
        bot.polling(none_stop=True, interval=0.5, timeout=20)
    except Exception as e:
        print(f"Polling error: {e}")
        time.sleep(5)
