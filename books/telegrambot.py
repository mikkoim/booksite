from telegram.ext import Updater, CommandHandler
import requests
import re
import os

TOKEN = os.environ.get('TELEGRAM_KEY')

def get_url():
    contents = requests.get('https://random.dog/woof.json').json()    
    url = contents['url']
    return url

def bop(update, context):
    url = get_url()
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=url)
    
def main():
    updater = Updater(TOKEN, use_context=True)
    
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('bop',bop))
    
    updater.start_polling()
    updater.idle()
    
if __name__ == '__main__':
    main()