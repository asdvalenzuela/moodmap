import os
import pymongo
import json
import pickle
import pusher
from classifier.analyzeTweets import best_word_features, clean_and_tokenize
import datetime
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream

pusherClient = pusher.Pusher(
  os.environ.get('PUSHER_APP_ID'),
  os.environ.get('PUSHER_KEY'),
  os.environ.get('PUSHER_SECRET')
)

# this line is for heroku
# MONGO_URL = os.environ.get('MONGOHQ_URL')

#creates connection to db
conn = pymongo.MongoClient()
db = conn.tweet_database

f = open('classifier/NBclassifier.pickle', 'rb')
classifier = pickle.load(f)

# twitter OAuth process
auth = OAuthHandler(os.environ.get('TWITTER_CONSUMER_KEY'), os.environ.get('TWITTER_CONSUMER_SECRET'))
auth.set_access_token(os.environ.get('TWITTER_ACCESS_TOKEN'), os.environ.get('TWITTER_ACCESS_TOKEN_SECRET'))

def gmt_convert(time):
	return (time + 17) % 25

def parse_data(data):
	#timestamp field is for display purposes within the tweet popup
	timestamp_ms = ((int(data['timestamp_ms'])-28800000) /1000.0)
	return {
		'loc': data['coordinates']['coordinates'],
		'hour': gmt_convert(int(data['created_at'][11:13])), #hour field is for querying purposes
		'entities': data['entities'],
		'id': data['id'],
		'profile_img': data['user']["profile_image_url_https"],
		'id_str': data['id_str'],
		'text': data['text'],
		'screen_name': data['user']['screen_name'],
		'timestamp': datetime.datetime.fromtimestamp(timestamp_ms).strftime('%m/%d %H:%M:%S')
	}

def score_tweet_for_sentiment(tweet):
	token_list = clean_and_tokenize(tweet['text'])
	score = classifier.classify(best_word_features(token_list))
	tweet['score'] = score
	return tweet

def push_to_frontend(scored_tweet):
	pusherClient['tweet_map'].trigger('new_tweet', scored_tweet)

def insert_into_db(scored_tweet):
	db.saved_tweets_from_stream.insert(scored_tweet)

class listener(StreamListener):

	def on_data(self, data):
		"""On receiving data, parses tweet, analyzes for sentiment, pushes to frontend, and inserts into db."""
		data = json.loads(data)
		#ensures tweet has a geotag
		if ('coordinates' in data):
			if data['coordinates'] != None:
			#ensures geotag lies within the Bay Area
				if (-123 <= data['coordinates']['coordinates'][0] <= -120) and (36 <= data['coordinates']['coordinates'][1] <= 39):
					tweet = parse_data(data)
					scored_tweet = score_tweet_for_sentiment(tweet)
					push_to_frontend(scored_tweet)
					insert_into_db(scored_tweet)	
					return True
		else:
			return True

	def on_error(self,status):
		print status

twitterStream = Stream(auth, listener())
#locations parameter format [SWlong, SWlat, NWlong, NElat]
twitterStream.filter(locations=[-122.50,36.8,-121.75,37.8], languages=["en"])
