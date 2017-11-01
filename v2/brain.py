
# read <date>.input.csv
#	put each race in a array
#	loop
#  	call cal3f
#			read 3f.csv
#
#  	call cal2h
# 			read 2h.csv
#	write result <date>-bet.csv


import sys
import csv
import pandas as pd
from pymongo import MongoClient
from pandas.io.json import json_normalize

client = MongoClient('localhost:27017')
db = client.heroin2


def s1(rdate):
	if (db.game.find_one({"date" : rdate}) != None ): 
		print "found"
		return
	array = {}
	game = 1	
	y,m,d = rdate.split('-')
	filename =  '%s-%s-odd.csv' % (d,str(int(m)))
	print filename
	with open(filename,'r') as s1csv:
		game = 0
		for row in s1csv.readlines():
			item = row.split('\t')
			if item[0] == '1':
				game +=1
				name = item[2]
				curr,life,win = cal_curr_life_win(name)
				avgspeed = cal_speed(name)
				insert(rdate,game,item[0],item[2],curr,life,win,avgspeed)
			else:
				name = item[2]
				curr,life,win = cal_curr_life_win(name)
				avgspeed = cal_speed(name)
				insert(rdate,game,item[0],item[2],curr,life,win,avgspeed)

def cal_curr_life_win(name):
	with open('3factors.data','r') as factors:
		fact = csv.reader(factors, delimiter=';') 
		for row in fact: 
			if name == row[0]:
				curr = row[1]
				life = row[2]
				fir,sec,thi,tot = row[3].split('-')
				try:
					win = round(((float(fir)+float(sec)+float(thi))/float(tot)),4)
					return(curr,life,win)
				except:
					win = 0
					return(curr,life,win)

def cal_speed(name):
	counter = 0
	speed = []
	with open('2horse.data', 'r') as horses:
		hors = csv.reader(horses, delimiter=';')
		for row in hors:
			if (counter > 4):
				return(reduce(lambda x, y: x+y, speed)/len(speed))
				break
			if name == row[0]:
				if (len(row) > 2):
					if (row[16] != '--'):
						dist = row[5]
						mm,ss,ms = row[16].split('.')
						speed.append(float(dist)/(float(mm)*60+float(ss)))
						counter += 1
				else:
					pass
			else:
				pass



def insert(rdate,game,num,name,curr,life,win,avgspeed):
	db.game.insert_one(
		{
		"date": rdate,
		"rac" : game,
		"hor" : [
			{"num" : num,
			"name" : name,
			"curr" : curr,
			"life" : life,
			"win": win,
			"avgs": avgspeed }]
		}
	)


def s2(rdate):
	for x in range(1,13):
		cursor = db.game.find({'rac': x},{'_id':0})
		norm = json_normalize(list(cursor),'hor',['rac'])
		df = pd.DataFrame(norm)
		df['curr_rank'] = df['curr'].rank(ascending=True)
		df['life_rank'] = df['life'].rank(ascending=True)
		df['avgs_rank'] = df['avgs'].rank(ascending=False)
		df['wins_rank'] = df['win'].rank(ascending=False)
		df['weighted'] = ((df['curr_rank']*40 + df['life_rank']*10 + df['avgs_rank']*40 + df['wins_rank']*10)/100).rank(ascending=True)
		print df.loc[:,['rac','num','name','weighted']].sort_values('weighted')


def main():
	rdate = "2017-10-14"
	s1(rdate)
	s2(rdate)


if __name__ == '__main__':
	main()
