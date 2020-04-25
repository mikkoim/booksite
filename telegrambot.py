from telegram.ext import Updater, CommandHandler
import requests
import re
import os

import os
import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'booksite.settings'
django.setup()

from books.models import Bookmodel, Reviewmodel, Shelfmodel

TOKEN = os.environ.get('TELEGRAM_KEY')


def setuser(update, context):
    value = update.message.text.split(' ')[1]
    context.user_data['user_id'] = value

    update.message.reply_text('Used ID set to {}'.format(value))

def getuser(update, context):
    value = context.user_data['user_id'] 
    update.message.reply_text('Used ID is {}'.format(value))
    
def main():
    updater = Updater(TOKEN, use_context=True)
    
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('setuser',setuser))
    dp.add_handler(CommandHandler('getuser',getuser))
    
    updater.start_polling()
    updater.idle()
    
if __name__ == '__main__':
    main()