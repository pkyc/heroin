
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
        if counter > 3:
            break
        gethor(name,link)
        counter += 1
    return

def gethor(n,l):
    file = open('output.json', 'w')
    hjson = "{'NAME' : '" + n + "', 'LINK': '" + l + "'}"
    htmlfile = urllib2.urlopen(l)
    htmltext = htmlfile.read()
    soup = BeautifulSoup(htmltext,'html.parser')

    table = soup.find("table", {"class": "bigborder"})

    header = table.find_all("td", {"class": "hsubheader"})

    # horse in list []
    horsedict = []
    for h in header:
        h = h.text.strip().encode("utf-8")
        if h == "VideoReplay":
            pass
        else:
            horsedict.append(h)

    #testing#
    aout = open('a.out', 'w')
    for anya in horsedict:
       aout.write(anya+"\n")
 
    # td in list []
    tddict = []
    tds = table.find_all("td", {"class": "htable_eng_text"})
    hjson = hjson + ",{RACE: [{"
    for td in tds: 
        td = td.text.strip().encode("utf-8")
        if td == "(No Running Records in this season)":
           pass
        elif td == "":
           pass
        else:
           tddict.append(td)


    #testing#
    bout = open('b.out', 'a')
    bout.write(n+"\n")
    for anyb in tddict:
       bout.write(anyb+"\n")

    for i in xrange(1,len(tddict),17):
	if i>17:
           j = i%18
        else:
           j = i
        hjson = hjson + "'" + horsedict[j] + "':" + "'" +  tddict[i] + "' ,"

    print(hjson)
    #file.write(hjson)

readhor()
