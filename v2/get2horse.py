
# get2horse.py

import urllib2
import re
import pymongo
import json
import pandas as pd
from pymongo import MongoClient


client = MongoClient('localhost:27017')
db = client.heroin2

def gethor(db2h,n,l):
	try:
		data = pd.read_html(l,attrs=re.compile('bigborder'),header=0)
		df = data[0].dropna(axis=0, how='all')
		df = df.assign(name=n)
		df = df.rename(columns = {'Dist.': 'Dist'})
		df = df.rename(columns = {'Declar.Horse Wt.': 'DeclarHorseWt'})
		df = df.rename(columns = {'Rtg.': 'Rtg'})
		df = df.rename(columns = {'Act.Wt.': 'ActWt'})
		df = df.rename(columns = {'Pla.': 'Pla'})
		records = json.loads(df.T.to_json()).values()
		db[db2h].insert(records)
	except Exception as msg:
		print msg.message
		return	

