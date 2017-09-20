
#
# curl the jc web to get all the horse name 
# write to mongodb db: hname , collection: horse
#
import urllib2
import re
import string
import pymongo
from pymongo import MongoClient
from bs4 import BeautifulSoup

#link = 'http://www.hkjc.com/english/racing/selecthorsebychar.asp?ordertype=A'

def hor(input):
	client = MongoClient('localhost', 27017)
	db = client.hname   
	horse = db.horse
	
	ans = db.horse.find_one({"name": input}, {"_id": 0, "link": 1})
	print ans


input = raw_input()
hor(input)

