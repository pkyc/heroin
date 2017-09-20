
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

atoz = list(string.uppercase)
allhor = ([])


def hor(all):
    client = MongoClient('localhost', 27017)
    db = client.hname   
    horse = db.horse
    for a in all:
        link = 'http://www.hkjc.com/english/racing/' + a[0].encode("utf-8")
        id = a[0].encode("utf-8")[18:]
        name = a[1].encode("utf-8")
        result = db.horse.update({"name": name},{"$set": {"id": id, "name": name, "link": link}},upsert=True)
    return


for a in atoz:
    #-- grep all horse name from A to Z, store in allhor
    link = 'http://www.hkjc.com/english/racing/selecthorsebychar.asp?ordertype='+a
    htmlfile = urllib2.urlopen(link)
    htmltext = htmlfile.read()
    soup = BeautifulSoup(htmltext,'html.parser')
    for each in  soup.find_all(href=re.compile("^horse.asp")):
        allhor.append([each.get('href'),each.contents[0]])

hor(allhor)
print len(allhor)

