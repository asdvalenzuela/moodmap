import os
import pymongo
import time

conn = pymongo.MongoClient()
db = conn.tweet_database
stream_tweets = db.stream_tweets
search_tweets = db.search_tweets

import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import Cursor 

# consumer keys and access tokens for twitter OAuth
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')
 
# twitter OAuth process
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# create api 
api = tweepy.API(auth)

def getTweets():
	# queries twitter search api for tweets in SF
	for page in Cursor(api.search, lang="en", count=100, geocode="37.7516,-122.4477,3.5mi").pages(20):
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
		 
			search_tweets.insert(data)

	time.sleep(900)

# executes function every 15 minutes to avoid rate limits
while True:
	getTweets()



 
# the following code uses twitter stream API to get tweets from SF area
# class listener(StreamListener):

# 	def on_data(self, data):
# 		print data
# 		return True

# 	def on_error(self,status):
# 		print status

# twitterStream = Stream(auth, listener())
# #swlong, swlat, nelong, nelat
# twitterStream.filter(locations=[-122.50,36.8,-121.75,37.8], languages=None)
