
import urllib2
import re
import string
import pymongo
import json
import csv
from pymongo import MongoClient
from bs4 import BeautifulSoup
from bs4.element import NavigableString


def readhor():
    client = MongoClient('localhost', 27017)
    db = client.hname   
    horse = db.horse
    cursor = horse.find({})
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
	htmlfile = urllib2.urlopen(l)
	htmltext = htmlfile.read()
	soup = BeautifulSoup(htmltext,'html.parser')

	try:
	 	table = soup.find_all("table", {"class": "bigborder"})
	except Exception as msg:
		print msg.message
		return

	try:
		t0header = [t0header.text.strip().encode("utf-8") for t0header in table[0].find_all("td",{"class": "hsubheader"})]
		t0rows = ''
		for t0row in table[0].find_all("tr"):
			t0rows += n
			for t0val in t0row.find_all("td",{"class": "htable_eng_text"}):
				t0rows += ';' + t0val.text.encode("utf-8").replace("\n","").replace("\xc2","").replace("\xa0","").replace("\r\t","").strip()
			t0rows += '\n'
		file.write(t0rows)
	except Exception as msg:
		print msg.message
		return

	try:
		t1header = [t1header.text.strip().encode("utf-8") for t1header in table[1].find_all("td",{"class": "hsubheader"})]
		t1rows = ''
		for t1row in table[1].find_all("tr"):
			t1rows += n
			for t1val in t1row.find_all("td"):
				t1rows += t1val.text.encode("utf-8").replace("\n","").replace("\xc2","").replace("\xa0","").replace("\r\t","").strip() 
			t1rows += '\n'
		file.write(t1rows)
	except Exception as msg:
		print msg.message
		return

## Program start here
file= open('2horse.data', 'w',0)
#csvfile = csv.writer(file)
readhor()
