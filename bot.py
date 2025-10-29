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
user_orders = {}
user_addresses = {}

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
        # Create keyboard menu instead of inline menu
        markup = create_main_keyboard(lang)
        sent_message = bot.send_message(call.message.chat.id,
                                        "Төмендегілердің бірін таңдаңыз" if lang == 0 else "Choose one of the following",
                                        reply_markup=markup)
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

def create_main_keyboard(lang):
    """Create the main keyboard menu with web app button"""
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    # Web App button - this will allow sendData to work
    menu_button = types.KeyboardButton(
        "🌯🥤 Menu 🍔🥪" if lang == 0 else "🌯🥤 Menu 🍔🥪",
        web_app=types.WebAppInfo(
            url="https://yesdelivery-nu.vercel.app" if lang == 0 else "https://yesdelivery-nu.vercel.app/menu_en.html"
        )
    )

    # Other buttons
    change_location = types.KeyboardButton(
        "Мекенжайды өзгерту📍" if lang == 0 else "Change location📍"
    )
    change_language = types.KeyboardButton(
        "Тіл / Language"
    )

    markup.add(menu_button)
    markup.add(change_location, change_language)
    return markup

@bot.message_handler(func=lambda message: message.text in [
    "Мекенжайды өзгерту📍", "Change location📍", "Тіл / Language"
])
def handle_keyboard_buttons(message):
    """Handle keyboard button presses"""
    user_id = message.from_user.id
    lang = user_languages.get(user_id, 0)

    if message.text in ["Мекенжайды өзгерту📍", "Change location📍"]:
        # Request location again
        text_kazakh = "Мекен-жайымды жіберу"
        text_english = "Send my location"
        item1 = types.KeyboardButton(text_kazakh if lang == 0 else text_english, request_location=True)
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        markup.add(item1)
        bot.send_message(message.chat.id,
                         "Курьер жеткізу адресің білу үшін мекен-жайыңызды жіберіңіз" if lang == 0
                         else "Send your location so the courier knows your delivery address",
                         reply_markup=markup)

    elif message.text == "Тіл / Language":
        # Show language selection inline keyboard
        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton("Қазақ", callback_data="qz")
        item2 = types.InlineKeyboardButton("English", callback_data="en")
        markup.add(item1, item2)
        bot.send_message(message.chat.id,
                         "Тілді таңдаңыз / Choose language",
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

        # Update the keyboard with new language
        markup = create_main_keyboard(lang)
        bot.send_message(call.message.chat.id,
                         "Төмендегілердің бірін таңдаңыз" if lang == 0 else "Choose one of the following",
                         reply_markup=markup)

# ... rest of your existing code (handle_location, handle_web_app_data, etc.) remains the same ...
@bot.message_handler(content_types=['location'])
def handle_location(message):
    lang = user_languages.get(message.from_user.id, 0)
    latitude = message.location.latitude
    longitude = message.location.longitude

    if lang == 0:
        link = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}&zoom=18&addressdetails=1&accept-language=kk"
    else:
        link = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}&zoom=18&addressdetails=1&accept-language=en"

    try:
        with urllib.request.urlopen(link) as url:
            data = json.load(url)

        address = data.get('address', {})

        if lang == 0:
            address_parts = []
            if address.get('road'):
                address_parts.append(address['road'])
            if address.get('house_number'):
                address_parts.append(address['house_number'])
            if address.get('city') or address.get('town') or address.get('village'):
                address_parts.append(address.get('city') or address.get('town') or address.get('village'))

            display_address = ', '.join(address_parts) if address_parts else data.get('display_name', '')
        else:
            display_address = data.get('display_name', '')

        confirmation_text = "Осы мекенжай дұрыс па?: " + display_address if lang == 0 else f"Is this your location?: {display_address}"

        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton("Иә ✅" if lang == 0 else "Yes ✅", callback_data='yes')
        item2 = types.InlineKeyboardButton("Жоқ ⛔" if lang == 0 else "No ⛔", callback_data='no')
        markup.add(item1, item2)

        processing_message = bot.send_message(message.chat.id, '♻️Processing your request♻️', reply_markup=types.ReplyKeyboardRemove())
        bot.delete_message(chat_id=message.chat.id, message_id=processing_message.message_id)

        confirmation_message = bot.send_message(message.chat.id, confirmation_text, reply_markup=markup)
        confirmation_messages[message.from_user.id] = confirmation_message.message_id

        user_addresses[message.from_user.id] = display_address

    except Exception as e:
        logging.error(f"Error processing location: {e}")
        bot.send_message(message.chat.id,
                        "Мекенжайды өңдеу кезінде қате орын алды" if lang == 0
                        else "Error processing location")

@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    try:
        user_id = message.from_user.id
        lang = user_languages.get(user_id, 0)

        logging.info(f"Received web app data: {message.web_app_data.data}")

        order_data = json.loads(message.web_app_data.data)
        user_orders[user_id] = order_data

        order_text = format_order_message(order_data, lang)
        user_address = user_addresses.get(user_id, "Not specified")

        address_label = "Мекенжай:" if lang == 0 else "Address:"
        full_message = f"{order_text}\n\n{address_label} {user_address}"

        markup = types.InlineKeyboardMarkup()
        pay_btn = types.InlineKeyboardButton("Төлеу 💳" if lang == 0 else "Pay 💳", callback_data='pay_order')
        refuse_btn = types.InlineKeyboardButton("Бас тарту 🙅" if lang == 0 else "Refuse 🙅", callback_data='refuse_order')
        markup.add(pay_btn, refuse_btn)

        bot.send_message(message.chat.id, full_message, reply_markup=markup)
        logging.info(f"Order confirmation sent to user {user_id}")

    except Exception as e:
        logging.error(f"Error processing web app data: {e}")
        lang = user_languages.get(message.from_user.id, 0)
        bot.send_message(message.chat.id,
                        "Тапсырысты өңдеу кезінде қате орын алды" if lang == 0
                        else "Error processing order")

def format_order_message(order_data, lang):
    if not order_data:
        return "Тапсырыс бос" if lang == 0 else "Order is empty"

    items_text = "Тапсырыс:\n" if lang == 0 else "Your order:\n"
    total = 0

    for item in order_data:
        if item.get('count', 0) > 0:
            item_total = item.get('totalPrice', 0)
            items_text += f"{item['count']} x {item['name']} - {item_total}₸\n"
            total += item_total

    total_text = "Жалпы бағасы:" if lang == 0 else "Total price:"
    items_text += f"\n{total_text} {total}₸"

    return items_text

@bot.callback_query_handler(func=lambda call: call.data in ['pay_order', 'refuse_order'])
def handle_order_actions(call):
    user_id = call.from_user.id
    lang = user_languages.get(user_id, 0)

    if call.data == 'pay_order':
        order = user_orders.get(user_id)
        if order:
            bot.answer_callback_query(call.id,
                                    "Төлем өңделуде..." if lang == 0
                                    else "Processing payment...")

            bot.send_message(call.message.chat.id,
                           "Төлем өтті! Тапсырысыңыз дайындалуда. ✅" if lang == 0
                           else "Payment successful! Your order is being prepared. ✅")

            if user_id in user_orders:
                del user_orders[user_id]
        else:
            bot.answer_callback_query(call.id,
                                    "Тапсырыс табылмады" if lang == 0
                                    else "Order not found")

    elif call.data == 'refuse_order':
        if user_id in user_orders:
            del user_orders[user_id]

        bot.answer_callback_query(call.id,
                                "Тапсырыс болдырмалды ❌" if lang == 0
                                else "Order cancelled ❌")

        bot.send_message(call.message.chat.id,
                        "Сіз тапсырысты болдырмадыңыз. Жаңа тапсырыс беру үшін менюге өтіңіз." if lang == 0
                        else "You have cancelled the order. Go to the menu to place a new order.")

while True:
    try:
        bot.polling(none_stop=True, interval=0.5, timeout=20)
    except Exception as e:
        print(f"Polling error: {e}")
        time.sleep(5)
