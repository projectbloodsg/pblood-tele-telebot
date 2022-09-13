from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from decouple import config
import requests
import telebot

API_KEY = config('TESTING_API_KEY')
BASE_URL = config('BASE_URL')

bot = telebot.TeleBot(API_KEY)

def getFirst():
    response = requests.get("{base_url}/messages/root".format(base_url=BASE_URL))
    print(response)
    if response.status_code != 200:
        print("Result not found!")

    return response.json()

def getChild(id):
    response = requests.get("{base_url}/messages/child/{childId}".format(base_url=BASE_URL, childId=id))
    if response.status_code != 200:
        print("Result not found!")

    return response.json()

def gen_markup(id):
    try:
        response = getChild(id)
        #print(response)
        #if response == []:

        markup = InlineKeyboardMarkup()
        length = len(response)
        markup.row_width = length
        for i in range(length):
            markup.add(InlineKeyboardButton(response[i]["content"], callback_data = response[i]["message_id"]))
        return markup
    except Exception as e:
        print(e)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        response = getChild(call.data)
        bot.send_message(call.message.chat.id, response[0]['content'], reply_markup=gen_markup(response[0]['message_id']))
    except Exception as e:
        print(e)

@bot.message_handler(commands=['start'])
def start(message):
    try:
        question = getFirst()
        bot.send_message(message.chat.id, question[0]['content'], reply_markup=gen_markup(question[0]["message_id"]))
    except Exception as e:
        print(e)

bot.polling()