
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
    for a in cursor:
        link = a["link"].encode("utf-8")
        name = a["name"].encode("utf-8")
        #gethor(name,link)
    name = "AMAZING KIDS"
    link = "http://www.hkjc.com/english/racing/horse.asp?HorseNo=T179"
    gethor(name,link)

    return
#
# Get earch horse by their ID
# Use beautifulsoup to parse the content, grep the lastest races data in table
#
def gethor(n,l):
    file = open('./data/' + n + '.json', 'a')
    file.write("NAME :'" + n + "'")
    htmlfile = urllib2.urlopen(l)
    htmltext = htmlfile.read()
    soup = BeautifulSoup(htmltext,'html.parser')

    try:
       table = soup.find("table", {"class": "bigborder"})
       header = table.find_all("td", {"class": "hsubheader"})
    except:
       return

    # horse in list []
    horsedict = []
    for h in header:
        h = h.text.strip().encode("utf-8")
        if h == "VideoReplay":
            pass
        else:
            horsedict.append(h)

    # td in list []
    tddict = []
    tds = table.find_all("td", {"class": "htable_eng_text"})
    for td in tds: 
        td = td.text.strip().encode("utf-8")
        if td == "(No Running Records in this season)":
           pass
        elif td == "":
           pass
        else:
           tddict.append(td)


    for i in range(len(tddict)):
	if i>17:
           j = i%18
        else:
           j = i
        file.write(horsedict[j] + ":" + "'" +  tddict[i] + "'\n")

readhor()
