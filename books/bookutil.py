# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 15:02:57 2020

@author: Mikko Impiö
"""
import requests
import xml.etree.ElementTree as ET
import pandas as pd

from datetime import datetime

from .auth_keys import KEY

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
    
    
def get_read_shelf(user_id):
    read_url = '{}review/list?v=2&shelf=read&sort=date_read&key={}&id={}'.format(BASE, KEY, user_id)

    read_response = requests.get(read_url)
    read_xml = read_response.text
    
    return Shelf(read_xml)

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