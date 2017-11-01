
import urllib2
import re
import json
import pymongo
import nextracedate
from pymongo import MongoClient
import pandas as pd
from lxml import html

client = MongoClient('localhost:27017')
db = client.heroin2
keyword = ''

def main():
	date,venue = nextracedate.getnextdate()
	dbOdd = str(date)+'-odd'
	if len(date) == 1:
		date = '0'+date
	if(db[dbOdd].count() == 0):
		keyword = 'added'
		for i in range(1,13):
			try:
				link = 'http://bet.hkjc.com/racing/index.aspx?lang=EN&date=' + date + '&venue=' + venue + '&raceno=' + str(i)
				data = pd.read_html(link,attrs={'id': 'horseTable'},header=0)
				df = data[0].drop('T/P',axis=1)
				df = df.drop('Colour',axis=1)
				df = df.dropna(axis=0, how='any')
				df = df.assign(raceno=i)
				df = df.rename(columns = {'No.': 'No'})
				df = df.rename(columns = {'Wt.': 'Wt'})
				df = df.rename(columns = {'Body Wt.': 'Body Wt'})
				df = df.rename(columns = {'Rtg.': 'Rtg'})
				records = json.loads(df.T.to_json()).values()
				db[dbOdd].insert(records)
			except Exception as msg:
				print msg.message
	else:
		keyword = 'already exist'

	print "%i %s in %s" % (db[dbOdd].count(),keyword, dbOdd)

main()
