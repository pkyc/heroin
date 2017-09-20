
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
    #name = "AMAZING KIDS"
    #link = "http://www.hkjc.com/english/racing/horse.asp?HorseNo=A240"
    #gethor(name,link)

    return
#
# Get earch horse by their ID
# Use beautifulsoup to parse the content, grep the lastest races data in table
#
def gethor(n,l):
	print n
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
		t0rows = []
		for t0row in table[0].find_all("tr"):
			t0rows.append([t0val.text.encode("utf-8").replace("\n","").replace("\xc2","").replace("\xa0","").replace("\r\t","").strip() for t0val in t0row.find_all("td")])
		for t0row in t0rows:
			if (t0row == ['', '', '']):
				pass
			else:
				#t0row.insert(0,n)
				#file.write(str(t0row)+"\n")
				#csvfile.writerows(t0row)
				print t0row
	except Exception as msg:
		print msg.message
		return

	try:
		t1header = [t1header.text.strip().encode("utf-8") for t1header in table[1].find_all("td",{"class": "hsubheader"})]
		t1rows = []
		for t1row in table[1].find_all("tr"):
			t1rows.append([t1val.text.encode("utf-8").replace("\n","").replace("\xc2","").replace("\xa0","").replace("\r\t","").strip() for t1val in t1row.find_all("td")])
		for t1row in t1rows:
			#file.write(str(t1row)+"\n")
			#csvfile.writerows(t1row)
			print t1row
	except:
		print "t1header fail"
		return

## Program start here
file= open('2horse.data', 'w',0)
csvfile = csv.writer(file)
readhor()
