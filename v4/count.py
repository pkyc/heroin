import urllib2
import re
import json
import pymongo
import pprint
from pymongo import MongoClient
import pandas as pd
from bs4 import BeautifulSoup
from lxml import html
client = MongoClient('localhost:27017')
db = client.heroin2
from bson.son import SON

print 'r3 count : ' , db.r3.count()
days = len(db.r3.distinct('Date'))
races = len(db.r3.distinct('Date'))
print 'races in', days , 'days'
#print 'Horse is 1 : ', db.r3.aggregate({'Horse': { $range: [ 0, "$Horse", 10 ] }})
