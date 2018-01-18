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
db = client.test
counter13 = 0
counter14 = 0
counter15 = 0
counter16 = 0

for d1 in db.r3.find({'Unnamed: 13': {'$regex': '.*\..*\...'}}):
	h = d1['Horse']
	ft = d1['Unnamed: 13']
	db.r3.update_one({'Horse': d1['Horse'],'Date': d1['Date']},{'$set':{'Finish Time': ft}})
	counter13 +=1

print counter13

for d2 in db.r3.find({'Unnamed: 14': {'$regex': '.*\..*\...'}}):
	h = d2['Horse']
	ft = d2['Unnamed: 14']
	db.r3.update_one({'Horse': d2['Horse'],'Date': d2['Date']},{'$set':{'Finish Time': ft}})
	counter14 +=1

print counter14

for d3 in db.r3.find({'Unnamed: 15': {'$regex': '.*\..*\...'}}):
	h = d3['Horse']
	ft = d3['Unnamed: 15']
	db.r3.update_one({'Horse': d3['Horse'],'Date': d3['Date']},{'$set':{'Finish Time': ft}})
	counter15 +=1

print counter15

for d4 in db.r3.find({'Unnamed: 16': {'$regex': '.*\..*\...'}}):
	h = d4['Horse']
	ft = d4['Unnamed: 16']
	db.r3.update_one({'Horse': d4['Horse'],'Date': d4['Date']},{'$set':{'Finish Time': ft}})
	counter16 +=1

print counter16
