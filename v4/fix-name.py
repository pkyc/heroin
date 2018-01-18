import urllib2
import re
import json
import pymongo
import pprint
from pymongo import MongoClient
import pandas as pd
from bs4 import BeautifulSoup
from lxml import html
from bson.son import SON

client = MongoClient('localhost:27017')
db = client.heroin2
counter = 0

for d in db.r3.find({'Horse': {'$regex': '\\('}}):
	h = d['Horse']
	hname, hid = h.split('(')
	hid = hid.rstrip(')')
	db.r3.update_one({'Horse': d['Horse']},{'$set':{'Horse': hname, 'Horseid': hid}})
	counter +=1

print counter
