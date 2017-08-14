
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
    counter = 0
    for a in cursor:
        link = a["link"].encode("utf-8")
        name = a["name"].encode("utf-8")
        if counter > 1:
            break
        gethor(name,link)
        counter += 1
    return

def gethor(n,l):
    print(n,l)
    hjson = "{'NAME' : '" + n + "', 'LINK': '" + l + "'}"
    htmlfile = urllib2.urlopen(l)
    htmltext = htmlfile.read()
    soup = BeautifulSoup(htmltext,'html.parser')

    table = soup.find("table", {"class": "bigborder"})

    header = table.find_all("td", {"class": "hsubheader"})

    # horse in list []
    horsedict = []
    for h in header:
        horsedict.append(h.text.strip().encode("utf-8"))

    # td in list []
    tddict = []
    tds = table.find_all("td", {"class": "htable_eng_text"})
    for td in tds:
        tddict.append(td.text.strip().encode("utf-8"))
    tddict.remove("(No Running Records in this season)")
    print(len(tddict))

    for i in range(len(tddict)):
	if i>18:
           j = i%19
	   #print(">18", j)
    	   #print(horsedict[(j)])
        else:
           j = i
        print(horsedict[j]+":"+tddict[i])
        #print("tddict")


readhor()

