__author__ = 'Ahmed'
from pymongo import MongoClient
import json
import csv

client = MongoClient()


db = client.hotelinfo




csvfile = open('data/sub1.csv', 'r')

fieldnames = ("Text","HotelID","ReviewID","Service","Cleanliness","Sleep Quality","Rooms","Location","Value","Overall","Sentiment")
reader = csv.DictReader( csvfile, fieldnames)
i = 0
for row in reader:
    if i == 0:
        i+=1
        continue
    db.insight.insert(row)

    print i
