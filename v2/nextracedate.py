
import urllib2
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
