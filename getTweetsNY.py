import os
import pymongo
import time

conn = pymongo.MongoClient()
db = conn.tweet_database
stream_tweetsNY = db.stream_tweetsNY
search_tweetsNY = db.search_tweetsNY

import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import Cursor 

# consumer keys and access tokens for twitter OAuth
CONSUMER_KEY1 = os.environ.get('CONSUMER_KEY1')
CONSUMER_SECRET1 = os.environ.get('CONSUMER_SECRET1')
ACCESS_TOKEN1 = os.environ.get('ACCESS_TOKEN1')
ACCESS_TOKEN_SECRET1 = os.environ.get('ACCESS_TOKEN_SECRET1')
 
# twitter OAuth process
auth = OAuthHandler(CONSUMER_KEY1, CONSUMER_SECRET1)
auth.set_access_token(ACCESS_TOKEN1, ACCESS_TOKEN_SECRET1)

# create api 
api = tweepy.API(auth)

def getTweets():
	# queries twitter search api for tweets in NY
	for page in Cursor(api.search, lang="en", count=100, geocode="40.7041533,-73.91764719999998,10mi").pages(20):
	    for tweet in page:
			# adds relevant data from each tweet to search collection in twitter mongo db 
			data = {}
			data['created_at'] = tweet.created_at
			if tweet.coordinates:
				data['loc'] = tweet.coordinates["coordinates"]
			if tweet.place:
				data['place_type'] = tweet.place.place_type
				data['place_box_coordinates'] = tweet.place.bounding_box.coordinates
				data['place_name'] = tweet.place.full_name
				data['place_id'] = tweet.place.id
			data['entities'] = tweet.entities
			data['id'] = tweet.id
			data['id_str'] = tweet.id_str
			data['text'] = tweet.text
			data['screen_name'] = tweet.user.screen_name
		 
			search_tweetsNY.insert(data)

	time.sleep(900)

# executes function every 15 minutes to avoid rate limits
while True:
	getTweets()