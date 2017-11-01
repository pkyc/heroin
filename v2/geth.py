
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

atoz = list(string.uppercase)
client = MongoClient('localhost', 27017)
db = client.heroin2   
horse = db.horse

def geth():
	for a in atoz:
		#-- grep all horse name from A to Z, store in allhor
		link = 'http://www.hkjc.com/english/racing/selecthorsebychar.asp?ordertype='+a
		htmlfile = urllib2.urlopen(link)
		htmltext = htmlfile.read()
		soup = BeautifulSoup(htmltext,'html.parser')
		for each in soup.find_all(href=re.compile("^horse.asp")):
			link = 'http://www.hkjc.com/english/racing/' + each.get('href')
			id = each.get('href')[18:]
			name = each.contents[0]
			result = db.horse.update({"name": name},{"$set": {"id": id, "name": name, "link": link}},upsert=True)
	print db.horse.count(),'updated'


geth()

