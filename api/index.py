from binance import Client
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
from telegram import Update
from dotenv import load_dotenv
import re
import os

load_dotenv()

TELEGRAM_BOT_TOKEN = GCP_PROJECT_ID = os.getenv('TELEGRAM_BOT_TOKEN')
updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)

def get_price(_symbol):
	price = '';
	try:
		client = Client()
		client.API_URL = 'https://api.binance.com/api'
		price += f'{_symbol}: $' + str(float(client.get_symbol_ticker(symbol=f'{_symbol}USDT')['price']))
	except Exception as e:
		price += 'Not found this coin'
		# print(f'Error: {e}')

	return price

def start(update: Update, context: CallbackContext):
	update.message.reply_text(
        "Hello sir, Welcome to the Bot.Please write\
        coin Symbol to see Price.")

def coin_price(update: Update, context: CallbackContext):
	symbol = re.sub(r"[^a-zA-Z0-9]","",update.message.text).upper()
	price = get_price(symbol)
	update.message.reply_text(price)

def main()
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, coin_price))
    updater.start_polling()
    updater.idle()

main()