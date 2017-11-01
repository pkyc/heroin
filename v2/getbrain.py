
import sys
import csv
import pandas as pd
from pymongo import MongoClient
from pandas.io.json import json_normalize
import nextracedate

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

client = MongoClient('localhost:27017')
db = client.heroin2

date,venue = nextracedate.getnextdate()
if len(date) == 1:
	date = '0'+date

def s1(date):
	dbOdd = str(date)+'-odd'
	for game in range (1,13):
		data = db[dbOdd].find({'raceno': game},{'_id':0,'Horse':1})
		for a in data:
			## Step here #################
			name = a.text
			print name
			curr,life,win = cal_curr_life_win(name)
		#avgspeed = cal_speed(name)
		#insert(date,game,item[0],item[2],curr,life,win,avgspeed)

def cal_curr_life_win(name):
		db3f = str(date)+'-3f'
		data = db[db3f].find({'name': name},{'_id':0, 'factor':1})
		for row in data: 
			try:
				print row
				#win = round(((float(fir)+float(sec)+float(thi))/float(tot)),4)
				#return(curr,life,win)
			except:
				print row
				#win = 0
				#return(curr,life,win)

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
			elif counter > 0 and counter < 4:
				return(reduce(lambda x, y: x+y, speed)/len(speed))
			else:
				pass



def insert(date,game,num,name,curr,life,win,avgspeed):
	db[date].insert_one(
		{
		"date": date,
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


def s2(date):
	for x in range(1,13):
		cursor = db[date].find({'rac': x},{'_id':0})
		norm = json_normalize(list(cursor),'hor',['rac'])
		df = pd.DataFrame(norm)
		df['num_int'] = df['num'].astype(int)
		df['curr_rank'] = df['curr'].astype(int).rank(ascending=True)
		df['life_rank'] = df['life'].astype(int).rank(ascending=True)
		df['avgs_rank'] = df['avgs'].rank(ascending=True)
		df['wins_rank'] = df['win'].rank(ascending=True)
		df['A'] = ((df['curr_rank']*60 + df['life_rank']*25 + df['avgs_rank']*10 + df['wins_rank']*5)/100).rank(ascending=True)
		df['B'] = ((df['curr_rank']*60 + df['life_rank']*10 + df['avgs_rank']*5 + df['wins_rank']*25)/100).rank(ascending=True)
		df['C'] = ((df['curr_rank']*5 + df['life_rank']*10 + df['avgs_rank']*25 + df['wins_rank']*60)/100).rank(ascending=True)
		df['D'] = ((df['curr_rank']*10 + df['life_rank']*5 + df['avgs_rank']*60 + df['wins_rank']*25)/100).rank(ascending=True)
		df['E'] = ((df['curr_rank']*25 + df['life_rank']*5 + df['avgs_rank']*60 + df['wins_rank']*10)/100).rank(ascending=True)
		df.loc[:,['rac','num_int','name','A','B','C','D','E']].sort_values('num_int').to_csv(path_or_buf='a.csv',mode='a',sep=';')


def main():
	s1(date)
	#s2(date)


if __name__ == '__main__':
	main()
