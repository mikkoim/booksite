# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 15:02:57 2020

@author: Mikko Impiö
"""
import requests
import xml.etree.ElementTree as ET
import pandas as pd
import os

from datetime import datetime

KEY = os.environ.get('GOODREADS_SECRET_KEY')

DATE_FORMAT = "%a %b %d %H:%M:%S %z %Y"
BASE = 'https://www.goodreads.com/'

class Book:
    def __init__(self, element):
        c = element.getchildren()
        
        # title
        self.title = c[5].text
        
        # image url
        self.image_url = c[7].text
        
        # number of pages
        num_pages = c[11].text
        if num_pages:
            num_pages = int(num_pages)
        self.num_pages = num_pages
            
        # publication year
        self.publication_year = c[16].text
        
        # average rating
        average_rating = c[18].text
        if average_rating:
            average_rating = float(average_rating)
        self.average_rating = average_rating
        
        #ratings count
        ratings_count = c[19].text
        if ratings_count:
            ratings_count = int(ratings_count)
        self.ratings_count = ratings_count
        
        # author
        auth = c[21].getchildren()[0].getchildren() 
        self.author = auth[1].text

    def __repr__(self):
        return self.title
    
def parse_datetime(datestring):
    if not datestring:
        return None
    else:
        dt = datetime.strptime(datestring, DATE_FORMAT)
        return dt.date()
        
class Review:
    def __init__(self, element):
        
        c = element.getchildren()
        self.book = Book(c[1])
        self.rating = float(c[2].text)
         
        self.started_at = parse_datetime(c[9].text)
        self.read_at = parse_datetime(c[10].text)
        
    def __repr__(self):
        s = "Book:\t\t\t\"{}\"\n" \
            "Author:\t\t\t{}\n" \
            "Avg rating:\t\t{}\n" \
            "User rating:\t{}\n" \
            "Started:\t\t{}\n" \
            "Read:\t\t\t{}".format(self.book.title,
                                   self.book.author,
                                   self.book.average_rating,
                                   self.rating,
                                   self.started_at,
                                   self.read_at)
        return s
    
class Shelf:
    def __init__(self, xml):
        self.root = ET.fromstring(xml)
        if self.root.text == 'Page not found':
            self.name = ''
            self.reviews = []
        else:
            self.name = dict(self.root[1].items())['name']
            
            review_elements = self.root[2].getchildren()
        
            self.reviews = [Review(element) for element in review_elements]
            
    def __getitem__(self, key):
        return self.reviews[key]
    def __repr__(self):
        s = "{}: {} books".format(self.name, len(self.reviews))
        return s
    
def get_shelves_list(user_id):
    url = '{}shelf/list.xml?key={}&user_id={}'.format(BASE,
                                                      KEY,
                                                      user_id)
    response = requests.get(url)
    xml = response.text
    
    root = ET.fromstring(xml)
    shelf_elements = root[1].getchildren()
    
    shelf_list = [e[1].text for e in shelf_elements]
    
    return shelf_list

def get_shelf(user_id, shelfname):
    
    if shelfname=='read':
        sort='date_read'
        per_page = '20'
    else:
        sort='rating'
        per_page='200'
        
    shelf_url = '{}review/list?v=2' \
                        '&shelf={}' \
                        '&key={}' \
                        '&id={}' \
                        '&sort={}' \
                        '&per_page={}'.format(BASE, 
                                            shelfname, 
                                            KEY, 
                                            user_id,
                                            sort,
                                            per_page)

    shelf_response = requests.get(shelf_url)
    shelf_xml = shelf_response.text
    
    return Shelf(shelf_xml)

def shelf_to_df(shelf):
    
    dicts = []
    for review in shelf.reviews:
        
        d = vars(review)
        d.update(vars(review.book))
        
        dicts.append(d)
    
    df = pd.DataFrame(dicts)
    
    df = df.drop('book', axis=1)
    
    return df


def reviewlist_to_df(reviewlist):
    d= {}
    d['rating'] = [r.rating for r in reviewlist]
    d['started_at'] = [r.started_at for r in reviewlist]
    d['read_at'] = [r.read_at for r in reviewlist]

    booklist = [r.book for r in reviewlist]

    d['title'] = [b.title for b in booklist]
    d['image_url'] = [b.image_url for b in booklist]
    d['num_pages'] = [b.num_pages for b in booklist]
    d['publication_year'] = [b.publication_year for b in booklist]
    d['average_rating'] = [b.average_rating for b in booklist]
    d['author'] = [b.author for b in booklist]

    return pd.DataFrame(d)
