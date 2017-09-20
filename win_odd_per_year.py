
#
# calculate the win_odd_per_year WINO
# 
# input the <date>.game , read horse name,
# input the 2factors.data, search the correlated horse name, calcualte the win_odd_per_yaer
#
#race1
#1       A FAST ONE      133     D Whyte 10      D E Ferraris    40      1       1114    1.10.09
#2       SKY TREASURE    133     J Moreira       8       Y S Tsui        40      -1      1067    1.10.37

import urllib2
import re
import string
import csv
import pymongo
from pymongo import MongoClient
from bs4 import BeautifulSoup


def cal_123(name):
	with open('3factors.data','r') as one23:
		for one23line in one23:
			if re.match(name, one23line):
				a,b,c,d = one23line.split(';')
				first,second,third,total = d.split('-')
				avgwin = (float(first) + float(second) + float(third)) / float(total)
				return(b,c,avgwin)

def cal_pace(name):
	print name
	with open('2horse.data','r') as h:
		hor = csv.reader(h, delimiter=',',quoting=True)
		for horline in hor:
			if name in horline:
				print horline[0]
	return()


def WINO(game_file):
	with open(game_file,'r') as games, open('3factors.data','r') as factors:
		for line in games:
			if (len(line.split('\t')) == 1):
				game_no = line.split()
			else:
				#no,name,jwt,jockey,trainer,rank,rankchange,hwt,besttime,gear,piority = line.split("\t")
				racedetails = line.split("\t")
				name = racedetails[1]
				pace = cal_pace(name)
				cur_win, total_win, avgwin = cal_123(name)
				#print name, cur_win, total_win, avgwin, pace

#game_file = raw_input()
game_file = '6-9.game'
WINO(game_file)

