import re
import os
from flask import Flask, request
from binance import Client
import telegram
from dotenv import load_dotenv

load_dotenv()
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
bot_user_name = "Coin Price"
URL =  os.getenv('SITE_URL')

global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

def get_price(_symbol):
    print(_symbol)
    price = ''
    try:
        client = Client()
        client.API_URL = 'https://api.binance.com/api'
        price += f'{_symbol}: $' + str(float(client.get_symbol_ticker(symbol=f'{_symbol}USDT')['price']))
    except Exception as e:
        price += 'Not found this coin'

    return price

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
   # retrieve the message in JSON and then transform it to Telegram object
   update = telegram.Update.de_json(request.get_json(force=True), bot)

   chat_id = update.message.chat.id
   # msg_id = update.message.message_id

   # Telegram understands UTF-8, so encode text for unicode compatibility
   text = update.message.text.encode('utf-8').decode()
   # for debugging purposes only
   print("got text message :", text)
   # the first time you chat with the bot AKA the welcoming message
   if text == "/start":
       # print the welcoming message
       bot_welcome = """
       Welcome to Coin Price Bot, the bot is using the service from Binance.com to get Coin price
       """
       # send the welcoming message
       # bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)
       bot.sendMessage(chat_id=chat_id, text=bot_welcome)


   else:
       try:
           symbol = re.sub(r"[^a-zA-Z0-9]","",text).upper()
           price = get_price(symbol)
           bot.sendMessage(chat_id=chat_id, text=price)
       except Exception:
           # if things went wrong
           bot.sendMessage(chat_id=chat_id,text="Please type corret coin symbal")

   return 'ok'

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
   s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
   if s:
       return "webhook setup ok"
   else:
       return "webhook setup failed"


if __name__ == '__main__':
   app.run(threaded=True)