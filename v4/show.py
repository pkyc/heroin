import urllib2
import re
import json
import pymongo
import nextracedate
from pymongo import MongoClient
import pandas as pd
from bs4 import BeautifulSoup
from lxml import html

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

client = MongoClient('localhost:27017')

###
test = client.test
print 'r3 count : ' , test.r3.count()
r_nums = test.r3.distinct('Race No')
print 'No. of race' , r_nums

for r_num in r_nums:
	cursor = test.r3.find({'Race No': r_num},{'_id': 0,'Horse':1, 'Jockey':1,'Trainer':1})
	df = pd.DataFrame(list(cursor))
	print df

###
heroin2 = client.heroin2
collection = 'odd-07-01-2018'
print 'odd count : ' , heroin2[collection].count()

r_nums = heroin2[collection].distinct('Race No')
print 'No. of race' , r_nums

for r_num in r_nums:
	cursor = heroin2[collection].find({'Race No': r_num},{'_id': 0,'Horse':1, 'Jockey':1,'Trainer':1})
	df = pd.DataFrame(list(cursor))
	print df
