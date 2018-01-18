import re
import json
import pymongo
from pymongo import MongoClient

client = MongoClient('localhost:27017')
db = client.test
counter = 0

#db.r3.delete({'Jockey': '1'})

for d in db.r3.find({}):
	if d['Jockey'].isdigit():
		db.r3.delete_one({'_id': d['_id']})
		counter +=1
	
	if d['Horse'].isdigit():
		db.r3.delete_one({'_id': d['_id']})
		counter +=1

	if d['Trainer'].isdigit():
		db.r3.delete_one({'_id': d['_id']})
		counter +=1

print counter
