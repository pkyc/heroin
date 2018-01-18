
# getResult.py
# schedule run by crontab , get the current race result
import sys
import csv
import urllib2
import re
import os
import json
import pymongo
import logging
import nextracedate
from pymongo import MongoClient
from bs4 import BeautifulSoup
import pandas as pd
from lxml import html

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(levelname)s %(message)s',filename='GetResult.log',filemode='w')

client = MongoClient('localhost:27017')
#db = client.heroin2
db = client.test
pwd = os.getcwd()


def getRDayInfo(link):
	try:
		htmlfile = urllib2.urlopen(link)
		htmltext = htmlfile.read()
		soup = BeautifulSoup(htmltext, 'html.parser')
		RD_table = soup.find("table").findNext("table").find_all("a", href=True)
		t1list = []
		for t1 in RD_table:
			t1list.append(t1['href'])
		t1list = t1list[:-1]
		t1list.insert(0,link[22:])
		return(t1list) #return each race link
	except Exception as msg:
		logging.debug('DayInfo failed' + ';' + msg.message)

def getRDayDetail(t1list):
	for t1 in t1list:
		link = "http://racing.hkjc.com" + t1
		rDate = t1.split('/')[7]
		rCourse = t1.split('/')[8]
		rNo = t1.split('/')[9].strip()
		try:
			htmlfile = urllib2.urlopen(link)
			htmltext = htmlfile.read()
			soup = BeautifulSoup(htmltext, 'html.parser')
			tb2 = soup.find("table").findNext("table").findNext("table").findNext("table").find_all("td")
			if len(tb2[0].text.split(' - ')) == 3:
				rClass,rDist,rCode = tb2[0].text.split(' - ')
			else:
				rClass,rDist = tb2[0].text.split(' - ')
				rCode = tb2[1].text
			trackCondition = tb2[2].text
			if len(tb2[5].text.split(' - ')) == 2:
				trackType,trackName  = tb2[5].text.split(' - ')
			else:
				trackType = tb2[5].text
				trackName = 'NA'
			data = pd.read_html(link,match='Plc.',header=0)
			df = data[0]
			df['Date'],df['Course'],df['Race No'] = [rDate, rCourse, rNo]
			df['Class'],df['Distant'],df['Code'] = [rClass, rDist, rCode]
			df['Track Condition'],df['Track Type'],df['Track Name'] = [trackCondition,trackType,trackName]
			df = df.rename(columns = {'\n                    Plc.\n                ': 'Plc'})
			df = df.rename(columns = {'\n                    Horse No.\n                ': 'Horse No'})
			df = df.rename(columns = {'\n                    Horse\n                ': 'Horse'})
			df = df.rename(columns = {'\n                    Jockey\n                ': 'Jockey'})
			df = df.rename(columns = {'ActualWt.': 'ActualWt'})
			df = df.rename(columns = {'Declar.Horse Wt.': 'Declar Horse Wt'})
			df = df.dropna(subset=['Trainer'])
			#df['Hore ID'] = df['Horse'].split('(').tolist()
			print json.loads(df.T.to_json()).values()
			db.r3.insert(json.loads(df.T.to_json()).values())
			logging.info('inserted;' + rDate + ';' + rNo)
		except Exception as msg:
			logging.error('insert error;' + t1 + ';' +  msg.message)


def main():
	file = pwd+'/run-date'
	with open(file,'r') as rundate:
		d,v = rundate.readline().split(' ')
		dd,mm,yy = d.split('-')
		if (len(dd) == 1):
			dd = '0'+str(dd)
		link = 'http://racing.hkjc.com/racing/info/meeting/Results/English/Local/' + str(yy) + str(mm) + str(dd) + '/' + v.strip() + '/1' 
		print link
		try:
			t1list = getRDayInfo(link)
			getRDayDetail(t1list)
		except Exception as msg:
			logging.error('main exception' + ';' + v.strip() + ';' +  msg.message)
main()
