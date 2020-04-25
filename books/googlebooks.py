#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import os
from io import StringIO
import json

KEY = os.environ.get('GOOGLE_BOOKS_KEY')
BASE = 'https://www.googleapis.com/books/v1/'


def make_query(query):
    url = '{}volumes?q={}'\
                    '&key={}'.format(BASE, query, KEY)
    response = requests.get(url)
    
    io = StringIO(response.text)
    j = json.load(io)
    
    return j['items'][0]

def get_isbn(book):
    try:
        ids = book['volumeInfo']['industryIdentifiers']
        types = [i['type'] for i in ids]
        
        if 'ISBN_13' in types:
            isbn = ids[types.index('ISBN_13')]['identifier']
            return isbn
        else:
            return None
    except KeyError:
        return None
    
def get_price(book):
    try:
        return book['saleInfo']['listPrice']['amount']
    except KeyError:
        return None