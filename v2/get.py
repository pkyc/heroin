
import urllib2
import re
import string
import pymongo
import json
import csv
from pymongo import MongoClient
from bs4 import BeautifulSoup
from bs4.element import NavigableString
import geth
import get2horse
import get3factors
import nextracedate


def readhor(date):
	db3f = str(date)+'-3f'
	db2h = str(date)+'-2h'
	client1 = MongoClient('localhost', 27017)
	client2 = MongoClient('localhost', 27017)
	db1 = client1.hname   
	db2 = client2.heroin2   
	horse = db1.horse

	cursor = horse.find({})
	db3fflag = ''
	db2hflag = ''
	for a in cursor:
		link = a["link"].encode("utf-8")
		name = a["name"].encode("utf-8")

		if (db2[db3f].count() == 0):
			db3fflag = 1
			get3factors.gethor(db3f,name,link)
		elif (db3fflag == 1):
			get3factors.gethor(db3f,name,link)
		else:
			pass
			#print "%s is do nothing" % db3f

		if (db2[db2h].count() == 0):
			db2hflag = 1
			get2horse.gethor(db2h,name,link)
		elif (db2hflag == 1):
			get2horse.gethor(db2h,name,link)
		else:
			pass
			#print "%s is do nothing" % db2h
	print "%i in %s" % (db2[db3f].count(),db3f)
	print "%i in %s" % (db2[db2h].count(),db2h)


		

## Program start here
if __name__ == '__main__':
	date,venue = nextracedate.getnextdate()
	print "next race - %s at %s" % (date, venue)
	geth.geth()
	readhor(date)
