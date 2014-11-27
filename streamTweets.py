import os
import pymongo
import json
import pickle
import pusher
from analyzeTweets import best_word_features, clean_and_tokenize
import time

p = pusher.Pusher(
  os.environ.get('PUSHER_APP_ID'),
  os.environ.get('PUSHER_KEY'),
  os.environ.get('PUSHER_SECRET')
)

#creates connection to db
conn = pymongo.MongoClient()
db = conn.tweet_database
stream = db.stream_tweets

f = open('NBclassifier.pickle', 'rb')
classifier = pickle.load(f)

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream

TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
# twitter OAuth process
auth = OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

class listener(StreamListener):

	def on_data(self, data):
		"""On receiving data, pushes to frontend and inserts into db."""
		data = json.loads(data)
		#ensures tweet has a geotag
		if ('coordinates' in data):
			if data['coordinates'] != None:
				#ensures geotag lies within the Bay Area
				if (-123 <= data['coordinates']['coordinates'][0] <= -120) and (36 <= data['coordinates']['coordinates'][1] <= 39):
					tweet = {}
					tweet['loc'] = data['coordinates']['coordinates']
					tweet['date'] = time.strftime("%m %d %y")
					tweet['hour'] = int(time.strftime("%H"))
					tweet['entities'] = data['entities']
					tweet['id'] = data['id']
					tweet['profile_img'] = data['user']["profile_image_url_https"]
					tweet['id_str'] = data['id_str']
					tweet['text'] = data['text'] 
					tweet['screen_name'] = data['user']['screen_name']
					#preprocess and score tweet for sentiment
					token_list = clean_and_tokenize(data['text'])
					score = classifier.classify(best_word_features(token_list))
					tweet['score'] = score
					#pushes to frontend
					p['tweet_map'].trigger('new_tweet', tweet)
					stream.insert(tweet)
					return True
		else:
			return True

	def on_error(self,status):
		print status

twitterStream = Stream(auth, listener())
#locations parameter format [SWlong, SWlat, NWlong, NElat]
twitterStream.filter(locations=[-122.50,36.8,-121.75,37.8], languages=["en"])
