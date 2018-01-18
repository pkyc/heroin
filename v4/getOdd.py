
import urllib2
import re
import json
import pymongo
import nextracedate
import datetime
from pymongo import MongoClient
from bs4 import BeautifulSoup
import pandas as pd
from lxml import html
from crontab import CronTab

client = MongoClient('localhost:27017')
db = client.heroin2
keyword = ''

def getRnum(comingdate,venue):
	link = 'http://bet.hkjc.com/racing/index.aspx?lang=EN&date=' + comingdate + '&venue=' + venue + '&raceno=1'
	htmlfile = urllib2.urlopen(link)
	htmltext = htmlfile.read()
	soup = BeautifulSoup(htmltext,'html.parser')
	Rnum = len(soup.find_all('td', {'class': 'raceButton'}))
	return(Rnum)
	
def main(comingdate,venue):
	dbOdd = 'odd-' + str(comingdate)
	if len(comingdate) == 1:
		comingdate = '0'+comingdate
	Rnum = getRnum(comingdate,venue)
	if(db[dbOdd].count() == 0):
		keyword = 'added'
		for i in range(1,Rnum+1):
			try:
				link = 'http://bet.hkjc.com/racing/index.aspx?lang=EN&date=' + comingdate + '&venue=' + venue + '&raceno=' + str(i)
				htmlfile = urllib2.urlopen(link)
				htmltext = htmlfile.read()
				soup = BeautifulSoup(htmltext,'html.parser')
				js = soup.find('table',attrs={'style' : 'PADDING-RIGHT:5px;PADDING-LEFT:0px;PADDING-BOTTOM:3px;PADDING-TOP:3px'}).text
				if (js.count(',') == 5):
					racename,rdate,rtime,rClass,trackType,rDist = js.split(',')
					trackName = trackType
					trackCondition = 'na'
				elif (js.count(',') == 7):
					racename,rdate,rtime,rClass,trackType,trackName,rDist,trackCondition = js.split(',')

				data = pd.read_html(link,attrs={'id': 'horseTable'},header=0)
				df = data[0].drop('T/P',axis=1)
				df = df.drop('Colour',axis=1)
				df = df.dropna(subset=['Jockey'])
				df = df.rename(columns = {'No.': 'No'})
				df = df.rename(columns = {'Wt.': 'Wt'})
				df = df.rename(columns = {'Body Wt.': 'Body Wt'})
				df = df.rename(columns = {'Rtg.': 'Rtg'})
				df['Date'],df['Course'],df['Race No'] = [comingdate, venue, i]
				df['Class'],df['Distant'] = [rClass, rDist]
				df['Track Condition'],df['Track Type'],df['Track Name'] = [trackCondition.rstrip(),trackType,trackName]
				records = json.loads(df.T.to_json()).values()
				db[dbOdd].insert(records)
			except Exception as msg:
				print msg.message
	else:
		keyword = 'already exist'

	print "%i %s in %s" % (db[dbOdd].count(),keyword, dbOdd)

def addjob(d,m):
	myCron = CronTab(user='root')
	job = myCron.new(command='/root/heroin/v3/run-getResult.bash')
	job.hour.on(17)
	job.day.on(d)
	job.month.on(m)
	myCron.write()


if __name__ == "__main__":
	comingdate,venue = nextracedate.getnextdate()
	f = open('/root/heroin/v3/run-date','w')
	f.write("%s %s\n" % (comingdate,venue))
	f.close()
	d,m,y = comingdate.split('-')
	d0 = datetime.date(int(y),int(m),int(d))
	d1 = datetime.date.today()
	delta = d0 - d1
	main(comingdate,venue)
	if (delta.days == 0):
		main(comingdate,venue)
		addjob(d,m)
	else:
		print "%s at %s , %i days to go" % (comingdate, venue, delta.days)
