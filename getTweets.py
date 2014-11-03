import pymongo
from pymongo import MongoClient

client = MongoClient
db = client.tweet_database
stream = db.stream_tweets
search = db.search_tweets

import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream 

# Consumer keys and access tokens, used for OAuth
consumer_key = 'f8dZzs2Gd8BMXMSPUCBvVdg5C'
consumer_secret = 'n1g23aOftIsyaGRGvFXGOOpjzcHZFagq6bk9VRyj8wVhobRe3P'
access_token = '2851451905-r2t5xIvIMS2fU8896xiGw1ijI719sOFwsPvkzoH'
access_token_secret = '52MX5qpmoJVCDOugGsKLqNFBrBZWSZZK01cE5bZ4uyoa8'
 
# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creation of the actual interface, using authentication
api = tweepy.API(auth)

results = api.search(geocode="37.781157,-122.398720,.5mi")

for result in results:
	search.insert(result)
 
# class listener(StreamListener):

# 	def on_data(self, data):
# 		print data
# 		return True

# 	def on_error(self,status):
# 		print status

# twitterStream = Stream(auth, listener())
# #swlong, swlat, nelong, nelat
# twitterStream.filter(locations=[-122.50,36.8,-121.75,37.8], languages=None)
