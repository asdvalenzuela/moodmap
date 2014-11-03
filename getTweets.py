import os
import pymongo

conn = pymongo.MongoClient()
db = conn.tweet_database
stream_tweets = db.stream_tweets
search_tweets = db.search_tweets

import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream 

# Consumer keys and access tokens, used for OAuth
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')
 
# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Creation of the actual interface, using authentication
api = tweepy.API(auth)

results = api.search(geocode="37.781157,-122.398720,.5mi")

for result in results:
	search_tweets.insert(result)
 
# class listener(StreamListener):

# 	def on_data(self, data):
# 		print data
# 		return True

# 	def on_error(self,status):
# 		print status

# twitterStream = Stream(auth, listener())
# #swlong, swlat, nelong, nelat
# twitterStream.filter(locations=[-122.50,36.8,-121.75,37.8], languages=None)
