#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from io import StringIO
import json


BASE = 'https://api.finna.fi/v1/'

def make_query(query, building=None):
    url = '{}search?lookfor={}'.format(BASE, query)
    
    if building:
        url = url + '&filter[]=building:{}'.format(building)
        
    response = requests.get(url)
    
    io = StringIO(response.text)
    
    return json.load(io)

def get_locations(response):
    try:
        records = response['records']
        locations = {}
        
        for r in records:
            title = r['title']
            buildings = [b['translated'] for b in r['buildings'][1:]]
            
            locations[title] = buildings
        return locations
    except KeyError:
        return None
        