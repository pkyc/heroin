
import sys
import csv

output = open('info2.data', 'w')

with open('info.data', 'r') as infile:
	lines = infile.readlines()
	for i in range(0, len(lines)):
		line = lines[i]
		if (i%4 == 0):
			n,name = line.split(":")
		elif (i%4 == 1):
			ss,seasonstakes = line.split(":")
		elif (i%4 == 2):
			ts,totalstakes = line.split(":")
		elif (i%4 == 3):
			ott,ottstarts = line.split(":")
			print name.strip()+';'+seasonstakes.strip()+';'+totalstakes.strip()+';'+ottstarts.strip()



