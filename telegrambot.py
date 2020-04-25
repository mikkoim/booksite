from telegram.ext import Updater, CommandHandler
import requests
import re
import os

import os
import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'booksite.settings'
django.setup()

from books.models import Bookmodel, Reviewmodel, Shelfmodel, Locationmodel
from books import bookutil

TOKEN = os.environ.get('TELEGRAM_KEY')

def bookquery_to_string(book_q):
    # Get titles and shorten them
    titlelist = [b.title for b in book_q]
    maxlength = 30
    titlelist = [t if len(t) < maxlength else t[0:maxlength]+'...' for t in titlelist]
    
    # Ratings
    ratinglist = [b.average_rating for b in book_q]

    # Combine and send
    stringlist = ["{} - \t{}".format(r[0],r[1]) for r in zip(titlelist, ratinglist)]
    
    return '\n'.join(stringlist)

def start(update, context):
    context.bot.send_message(update.message.chat_id,
    'Hello there!\n'
    'Welcome to the booksite bot! You can search for Goodreads shelves'\
    ' first searched on ohjsiha.herokuapp.com.'
    'Current commands are: \n' \
    '/setuser <User ID>: Sets the user ID\n' \
    '/getuser: Returns the current user ID\n' \
    '/shelves: Shelves searched on the website\n'\
    '/shelf <shelfname>: Returns top rated books on the shelf')

def setuser(update, context):
    value = update.message.text.split(' ')[1]

    if not Shelfmodel.objects.filter(user_id=value).exists():
        update.message.reply_text('User not found. Have you searched for it first on the web page?')
        return

    context.user_data['user_id'] = value
    update.message.reply_text('User ID set to {}'.format(value))

def getuser(update, context):
    value = context.user_data['user_id'] 
    update.message.reply_text('User ID is {}'.format(value))

def shelf(update, context):

    # Get shelf and books in it
    shelfname = update.message.text.split(' ')[1]
    user_id = context.user_data['user_id']
    try:
        shelf = Shelfmodel.objects.get(user_id=user_id,
                                            name=shelfname)
    except:
        update.message.reply_text('Shelf not found. ' \
            'Have you searched for it on the web page?'\
            'Found shelves are:')
        getshelves(update, context)
        return 
    book_q = [r.book for r in shelf.reviewmodel_set.order_by('-book__average_rating')]

    s = bookquery_to_string(book_q)
    update.message.reply_text(s)

def shelves(update, context):
    user_id = context.user_data['user_id']
    shelf_q = Shelfmodel.objects.filter(user_id=user_id)
    shelf_list = [shelf.name for shelf in shelf_q]
    s = '\n'.join(shelf_list)
    update.message.reply_text(s)

def places(update, context):
    location_q = Locationmodel.objects.all()
    locations = [loc.name for loc in location_q]
    s = '\n'.join(locations)
    update.message.reply_text(s)

def place(update, context):
    placename = update.message.text.split(' ')[1]
    location = Locationmodel.objects.get(name=placename)
    book_q = location.bookmodel_set.order_by('-average_rating')
    s = bookquery_to_string(book_q)
    update.message.reply_text(s)

def main():
    updater = Updater(TOKEN, use_context=True)
    
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('help', start))
    dp.add_handler(CommandHandler('setuser',setuser))
    dp.add_handler(CommandHandler('getuser',getuser))
    dp.add_handler(CommandHandler('shelf',shelf))
    dp.add_handler(CommandHandler('shelves',shelves))
    dp.add_handler(CommandHandler('places',places))
    dp.add_handler(CommandHandler('place',place))
    
    updater.start_polling()
    updater.idle()
    
if __name__ == '__main__':
    main()