
import urllib2
import datetime
from datetime import date
from pymongo import MongoClient
from bs4 import BeautifulSoup

# return this:
# date in 29-10-2017
# venue in 'HV' or 'ST'

def getnextdate():
	masterlink = 'http://bet.hkjc.com/racing/pages/odds_wp.aspx?lang=EN'
	htmlfile = urllib2.urlopen(masterlink)
	htmltext = htmlfile.read()
	soup = BeautifulSoup(htmltext,'html.parser')
	js = soup.find("script", {"type": "text/javascript"}).findNext("script").text
	link = js.split("'")[1]
	date = link.split("&")[1][5:] 
	venue = link.split("&")[2][6:]
	return(date,venue)

if __name__ == "__main__":
	comingdate,venue = getnextdate()
	d,m,y = comingdate.split('-')
	d0 = datetime.date(int(y),int(m),int(d))
	d1 = datetime.date.today()
	delta = d0 - d1
	print "%s at %s , %i days to go" % (comingdate, venue, delta.days)
	
