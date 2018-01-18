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

counter13 = 0
counter14 = 0
counter15 = 0
counter16 = 0

for d1 in db.r3.find({'Finish Time': '---'}):
	#print d1['Date'],d1['Horse'],d1['Unnamed: 14']
	print d1
	counter13 +=1

print counter13

