
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


def s1():
	array = {}
	game = 1	
	filename =  '13-9-input.csv'
	with open(filename,'r') as s1csv:
		game = 1
		for row in s1csv.readlines():
			item = row.split('\t')
			array = []
			arrayname = ''
			if item[0] == '1':
				arrayname = str(game) + str(item[0])
				array.append({arrayname,item[1]})
				game +=1
			else:
				arrayname = str(game) + str(item[0])
				array.append({arrayname,item[1]})

	print array


def main():
	s1()


if __name__ == '__main__':
	main()
