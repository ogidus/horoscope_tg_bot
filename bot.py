import os
import requests
import telebot
from telebot import types
import requests
import csv

BOT_TOKEN = ""

bot = telebot.TeleBot(BOT_TOKEN)

username =[]
ID = []
name = []
lname = []
mesaj = []


def get_daily_horoscope(sign: str, day: str) -> dict:
    url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"
    params = {"sign": sign, "day": day}
    response = requests.get(url, params)
    return response.json()

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.send_message(message.chat.id, "type /horoscope to get your horoscope for today")

@bot.message_handler(commands=['horoscope'])
def sign_handler(message):
    text = "What's your zodiac sign?"
    markup_inline = types.InlineKeyboardMarkup()
    item_Aries = 			types.InlineKeyboardButton(text = 'Aries', callback_data = 'ARIES')
    item_Taurus = 			types.InlineKeyboardButton(text = 'Taurus', callback_data = 'TAURUS')
    item_Gemini = 			types.InlineKeyboardButton(text = 'Gemini', callback_data = 'GEMINI')
    item_Cancer = 			types.InlineKeyboardButton(text = 'Cancer', callback_data = 'CANCER')
    item_Leo = 				types.InlineKeyboardButton(text = 'Leo', callback_data = 'LEO')
    item_Virgo = 			types.InlineKeyboardButton(text = 'Virgo', callback_data = 'VIRGO')
    item_Libra = 			types.InlineKeyboardButton(text = 'Libra', callback_data = 'LIBRA')
    item_Scorpio = 			types.InlineKeyboardButton(text = 'Scorpio', callback_data = 'SCORPIO')
    item_Sagittarius = 		types.InlineKeyboardButton(text = 'Sagittarius', callback_data = 'SAGITTARIUS')
    item_Capricorn = 		types.InlineKeyboardButton(text = 'Capricorn', callback_data = 'CAPRICORN')
    item_Aquarius = 		types.InlineKeyboardButton(text = 'Aquarius', callback_data = 'AQUARIUS')
    item_Pisces = 			types.InlineKeyboardButton(text = 'Pisces', callback_data = 'PISCES')
    markup_inline.add(item_Aries,item_Taurus,item_Gemini,item_Cancer, item_Leo, item_Virgo, item_Libra, item_Scorpio, item_Sagittarius, item_Capricorn,item_Aquarius,item_Pisces)
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup = markup_inline)


@bot.callback_query_handler(func = lambda call: True)
def fetch_horoscope(call):
	day = "TODAY"
	sign = call.data
	horoscope = get_daily_horoscope(sign, day)
	data = horoscope["data"]
	horoscope_message = f'*Horoscope:* {data["horoscope_data"]}\n*Sign:* {sign}\n*Day:* {data["date"]}'
	bot.send_message(call.message.chat.id , "Here's your horoscope!")
	bot.send_message(call.message.chat.id , horoscope_message, parse_mode="Markdown")


@bot.message_handler(func=lambda message: not message.entities and not message.caption_entities)
def echo_message(message):
    username.append(message.from_user.username)
    ID.append(message.from_user.id)
    name.append(message.from_user.first_name)
    lname.append(message.from_user.last_name)
    mesaj.append(message.text)
    with open('log.csv', 'a', buffering=1 ,encoding='UTF8', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(zip(username,ID,name,lname,mesaj))
    username.pop(0)
    ID.pop(0)
    name.pop(0)
    lname.pop(0)
    mesaj.pop(0)

bot.infinity_polling()
