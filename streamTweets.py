import os
import pymongo
import json

conn = pymongo.MongoClient()
db = conn.tweet_database
stream = db.stream_tweets

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream

# consumer keys and access tokens for twitter OAuth
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')
 
# twitter OAuth process
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# the following code uses twitter stream API to get tweets from the US
class listener(StreamListener):

	def on_data(self, data):
		data = json.loads(data)
		if ('coordinates' in data):
			if data['coordinates'] != None:
				tweet = {}
				tweet['created_at'] = data['created_at']
				tweet['loc'] = data['coordinates']['coordinates']
				tweet['entities'] = data['entities']
				tweet['id'] = data['id']
				tweet['id_str'] = data['id_str']
				tweet['text'] = data['text'] 
				tweet['screen_name'] = data['user']['screen_name']
				stream.insert(tweet)
				return True
		else:
			return True

	def on_error(self,status):
		print status

twitterStream = Stream(auth, listener())
#swlong, swlat, nelong, nelat
#this is for the entire USA: locations=[-124.848974, 24.396308,-66.885444, 49.384358]
twitterStream.filter(locations=[-122.50,36.8,-121.75,37.8], languages=["en"])
