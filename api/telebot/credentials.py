from dotenv import load_dotenv
import os
load_dotenv()
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
bot_user_name = "Coin Price"
URL =  os.getenv('SITE_URL')