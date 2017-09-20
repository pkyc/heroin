
import urllib2
import re
import string
import pymongo
import json
from pymongo import MongoClient
from bs4 import BeautifulSoup

def readhor():
    client = MongoClient('localhost', 27017)
    db = client.hname   
    horse = db.horse
    cursor = horse.find({})
    total = horse.count()
    for a in cursor:
        link = a["link"].encode("utf-8")
        name = a["name"].encode("utf-8")
        gethor(name,link)
    return
#
# Get earch horse by their ID
# Use beautifulsoup to parse the content, grep the lastest races data in table
#
def gethor(n,l):
	openner = urllib2.build_opener(urllib2.HTTPCookieProcessor())	
	htmlfile = openner.open(l)
	htmltext = htmlfile.read()
	soup = BeautifulSoup(htmltext,'html.parser')

	try:
		seasonstakes = soup.find(string="Season Stakes*").next_element.next_element.get_text().replace(": \r\n","").strip()
	except:
		seasonstakes = "$0"

	try:	
		totalstakes = soup.find(string="Total Stakes*").next_element.next_element.get_text().replace(": \r\n","").replace(": ","").strip()
	except:
		totalstakes = "$0"

	try:
		no123starts = soup.find(string=re.compile("of 1-2-3-Starts*")).next_element.next_element.get_text().replace(": \r\n","").replace(": ","").strip()
	except:
		no123starts = "ERROR"

	file.write(n + ";" + seasonstakes + ";" + totalstakes + ";" + no123starts + "\n")	



file = open("3factors.data",'w',0)
readhor()
