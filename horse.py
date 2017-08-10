
import urllib2
import re
import string
import pymongo
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
        if counter > 4:
            break
        gethor(name,link)
        counter += 1
    return

def gethor(n,l):
    print(n,l)
    htmlfile = urllib2.urlopen(l)
    htmltext = htmlfile.read()
    soup = BeautifulSoup(htmltext,'html.parser')
    table = soup.findChildren("table", {"class": "bigborder"})[0]
    header = table.findChildren("tr", {"bgcolor": "#CEE7FF"})
    print(header)
    tds = table.findChildren("td")
    for a in tds:
        print(a.text.strip())
    #print(tds.text.encode("utf-8").strip())

readhor()

