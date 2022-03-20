from cmath import nan
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
#from telebot.utils import quick_markup

API_KEY = "5127493459:AAE5mHB1lIYoLqSH7mllw1nvQLi2H89mQCo"
message_chat_id = 0

bot = telebot.TeleBot(API_KEY)


question1 = [{
    'id':'1',
    'text':"intro yadda yadda",
    'url': ''
}]

response1 = [
{
    'id':'2',
    'text':"yes",
    'url': ''
},
{
    'id':'3',
    'text':"no",
    'url': ''
}
]
question2 = [{
    'id':'4',
    'text':"question2",
    'url': ''
}]

response2 = [
{
    'id':'5',
    'text':"yes2",
    'url': ''
},
{
    'id':'6',
    'text':"no2",
    'url': ''
}
]

def getFirst():
    return question1

def getChild(id):
    if id == "1":
        return response1
    if id == "2":
        return question2
    if id == "3":
        return question1
    if id == "4":
        return response2

def gen_markup(id):
    response = getChild(id)
    markup = InlineKeyboardMarkup()#one_time_keyboard = True)
    length = len(response)
    markup.row_width = length
    for i in range(length):
        markup.add(InlineKeyboardButton(response[i]["text"], callback_data = response[i]["id"]))
    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    #global message_chat_id
    
    #print(call.message.chat.id)
    #print(message_chat_id)
    response = getChild(call.data)
    bot.send_message(call.message.chat.id, response[0]['text'], reply_markup=gen_markup(response[0]['id']))


@bot.message_handler(commands=['start'])
def start(message):
    #print(message.chat.id)
    
    #global message_chat_id 

    #message_chat_id = message.chat.id
    bot.send_message(message.chat.id, question1[0]['text'], reply_markup=gen_markup("1"))
    #bot.send_message(message.chat.id, "Yes/no?", reply_markup=gen_markup())


@bot.message_handler()#commands=['hello'])
def hello(message):
    if message.text == 'hello':
        bot.send_message(message.chat.id, "hello")

        #bot.send_message(message.chat.id, "Hello!")

bot.polling()