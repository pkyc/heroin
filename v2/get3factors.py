
# get3factors.py
import urllib2
import re
import string
import pymongo
import json
import nextracedate
from pymongo import MongoClient
from bs4 import BeautifulSoup

client = MongoClient('localhost:27017')
db = client.heroin2

# Get earch horse by their ID
# Use beautifulsoup to parse the content, grep the lastest races data in table
#
def gethor(db3f,n,l):
	openner = urllib2.build_opener(urllib2.HTTPCookieProcessor())	
	htmlfile = openner.open(l)
	htmltext = htmlfile.read()
	soup = BeautifulSoup(htmltext,'html.parser')

	try:
		seasonstakes = soup.find(string="Season Stakes*").next_element.next_element.get_text().replace(": \r\n","").strip()
		seasonstakes = seasonstakes.lstrip('$').replace(',','')
	except:
		seasonstakes = "0"

	try:	
		totalstakes = soup.find(string="Total Stakes*").next_element.next_element.get_text().replace(": \r\n","").replace(": ","").strip()
		totalstakes = totalstakes.lstrip('$').replace(',','')
	except:
		totalstakes = "0"

	try:
		no123starts = soup.find(string=re.compile("of 1-2-3-Starts*")).next_element.next_element.get_text().replace(": \r\n","").replace(": ","").strip()
	except:
		no123starts = "ERROR"

	db[db3f].insert_one(
	{
	"name": n,
	"factors": [
		{"seasonstakes": seasonstakes,
		"totalstakes": totalstakes,
		"no123starts": no123starts }]
		}	
	)

