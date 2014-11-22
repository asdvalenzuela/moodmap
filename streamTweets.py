import os
import pymongo
import json
import pickle
import pusher
from analyzeTweetsClean import best_word_features, clean_and_tokenize
import time

print time.strftime("%m %d %y")
print int(time.strftime("%H"))

p = pusher.Pusher(
  os.environ.get('PUSHER_APP_ID'),
  os.environ.get('PUSHER_KEY'),
  os.environ.get('PUSHER_SECRET')
)

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
				tweet['date'] = time.strftime("%m %d %y")
				tweet['hour'] = int(time.strftime("%H"))
				tweet['loc'] = data['coordinates']['coordinates']
				tweet['entities'] = data['entities']
				tweet['id'] = data['id']
				tweet['id_str'] = data['id_str']
				tweet['text'] = data['text'] 
				tweet['screen_name'] = data['user']['screen_name']
				token_list = clean_and_tokenize(data['text'])

				f = open('NBclassifier.pickle', 'rb')
				classifier = pickle.load(f)
				score = classifier.classify(best_word_features(token_list))
				f.close()

				tweet['score'] = score

				p['tweet_map'].trigger('new_tweet', tweet)
				stream.insert(tweet)
				return True
		else:
			return True

	def on_error(self,status):
		print status

twitterStream = Stream(auth, listener())
# #swlong, swlat, nelong, nelat
# #this is for the entire USA: locations=[-124.848974, 24.396308,-66.885444, 49.384358]
twitterStream.filter(locations=[-122.50,36.8,-121.75,37.8], languages=["en"])
