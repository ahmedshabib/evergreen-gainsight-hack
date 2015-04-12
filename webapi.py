__author__ = 'Ahmed'
import time
import calendar
from flask import Flask, request, session, g, redirect, url_for, render_template, flash
from pymongo import MongoClient
import json
import uuid
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
import random
from flask_oauth import OAuth
import math
from StringIO import StringIO

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('MYDIARY_SETTINGS', silent=True)
client = MongoClient()

db = client.hotelinfo



@app.route('/hotelinfo/')
def get_hotel_insight():
    hotelid = request.args.get("hotelid")
    reviews = db.insight.find({"HotelID":hotelid}, {"_id": 0})
    hotelinfo = db.hotels.find_one({"HotelInfo.HotelID":hotelid}, {"_id": 0})
    review_arr = [a for a in reviews]
    print review_arr
    print hotelinfo

    overallrating = 0
    sentiment =0
    hotelinfo["HotelInfo"]["Rating"] = 3
    hotelinfo["HotelInfo"]["Sentiment"] = 50

    total_reviews = len(review_arr)
    for i in range(total_reviews):
        overallrating += float(review_arr[i].get("Overall"))
        sentiment += int(review_arr[i]["Sentiment"])
        print sentiment
        if review_arr[i]["Sentiment"]  == '1' :
            review_arr[i]["Sentiment"] = True
        else:
            review_arr[i]["Sentiment"] = False
    if(len(review_arr) > 0):
        print str(total_reviews) + "I am"
        hotelinfo["HotelInfo"]["Rating"] = int(overallrating/total_reviews)
        hotelinfo["HotelInfo"]["Sentiment"] = math.ceil(sentiment*100.0/total_reviews)

    print hotelinfo["HotelInfo"]["Rating"]
    print hotelinfo["HotelInfo"]["Sentiment"]
    return render_template("hotelinfo.html",reviews=review_arr,hotelinfo=hotelinfo)


@app.route('/gethotelinfo/')
def get_hotel_info():
    hotelid = str(request.args.get("hotelid"))
    print hotelid
    out = db.hotels.find({"HotelInfo.HotelID":hotelid}, {"_id": 0})

    return json.dumps([a for a in out], indent=4)

@app.route('/search/')
def get_hotel_search():
    keyword = str(request.args.get("keyword"))
    print keyword
    text_results = db.command('text', 'hotels', search=keyword, limit=20)['results']
    doc_matches = [res['obj'] for res in text_results]
    return json.dumps([a["HotelInfo"] for a in doc_matches], indent=4)


@app.route('/')
def index():
    return render_template("index.html",error=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0',threaded=True)
