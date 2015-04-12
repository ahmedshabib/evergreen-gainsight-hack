__author__ = 'Ahmed'
from pymongo import MongoClient
import json
import re
from os import listdir
from os.path import isfile, join

client = MongoClient()


db = client.hotelinfo

j = 0

for i in  [ f for f in listdir('json') if isfile(join('json',f)) ]:
      if i.find(".json") == -1:
          continue
      print i
      hotel = {}
      try:
        hotelinfo = json.load(open('json/'+i))
      except:
        continue
      hotel["HotelInfo"] =  hotelinfo["HotelInfo"]
      reviews = hotelinfo["Reviews"]
      finalReviewList = []
      for i in range(len(reviews)):
          review ={}
          text = re.sub('[^A-Za-z0-9\.\s]+', '', reviews[i]["Content"])
          text = '"' +text + '"'
          try:
              review["Content"] = text
              review["ReviewID"] = reviews[i]["ReviewID"]
              review["Ratings"] = review[i]["Ratings"]
              review["Author"] = review[i]["Author"]
              review["AuthorLocation"] = review[i]["AuthorLocation"]
              review["Title"] = review[i]["Title"]
              review["Date"] = review[i]["Date"]
              finalReviewList.append(review)
          except:
              continue
      hotel["Reviews"] = finalReviewList
      db.hotels.insert(hotel)
      print j
      j+=1

