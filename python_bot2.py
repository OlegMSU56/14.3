import telebot
from telebot import types

# BOT tokeni
TOKEN = ""
bot = telebot.TeleBot(8365726426:AAHdMQiltMYonkTSenyiDSD8H0eK9EzHtRY)

# obuna bolish kerak bolgan kanallar
CHANNELS = [
    "@https://t.me/life_shokh",
]

# User kanallaga obuna bolganmi yoki yoq tekshrsh
def check_user(user_id):
    for ch in CHANNELS:
        try:
            status = bot.get_chat_member(ch, user_id).status
            if status in ['left', 'kicked']:
                return False
        except:
            return False
    return True

# obuna bolmagan bolsa sorov berish
def ask_to_subscribe(chat_id):
    markup = types.InlineKeyboardMarkup()

    for ch in CHANNELS:
        markup.add(types.InlineKeyboardButton(text=ch, url=f"https://t.me/{ch[1:]}"))

    markup.add(types.InlineKeyboardButton("tekshirish", callback_data="check"))

    bot.send_message(chat_id, "botdan foydalanish uchun kanallarga obuna boling", reply_markup=markup)

# start bosilganda
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if check_user(user_id):
        bot.send_message(message.chat.id, "botdan foydalanishingiz mumkin!")
    else:
        # agar obuna bolmagan bolsa
        ask_to_subscribe(message.chat.id)

# tekshrsh tugmasi bosilganda
@bot.callback_query_handler(func=lambda call: call.data == "check")
def check_callback(call):
    user_id = call.from_user.id
    if check_user(user_id):
        bot.send_message(call.message.chat.id, "botdan foydalanishingiz mumkin!")
    else:
        bot.send_message(call.message.chat.id, "barcha kanallarga obuna bolmagansiz!")

# har qanday habar kelganda tekshrsh
@bot.message_handler(func=lambda message: True)
def all_messages(message):
    user_id = message.from_user.id
    if not check_user(user_id):
        ask_to_subscribe(message.chat.id)
        return

    bot.send_message(message.chat.id, f"Siz yozdingiz: {message.text}")

bot.polling()

