from pymongo import MongoClient
import os
import pickle
from classifier.analyzeTweets import best_word_features, clean_and_tokenize
import tweepy
from tweepy import OAuthHandler
from tweepy import Cursor 

# tweet data in MongoDB is coming from streamTweets.py

# this line is for heroku
# MONGO_URL = os.environ.get('MONGOHQ_URL')

# creates connection to db
client = MongoClient()
db = client.tweet_database

# twitter OAuth process
auth = OAuthHandler(os.environ.get('TWITTER_CONSUMER_KEY'), os.environ.get('TWITTER_CONSUMER_SECRET'))
auth.set_access_token(os.environ.get('TWITTER_ACCESS_TOKEN'), os.environ.get('TWITTER_ACCESS_TOKEN_SECRET'))
# create api 
api = tweepy.API(auth)

f = open('classifier/NBclassifier.pickle', 'rb')
classifier = pickle.load(f)

def get_todays_tweets(current_hour):
    """Given the current hour, returns list of all tweets 
    up to the current hour.

    current_hour: integer between 0 and 24
    """
    tweet_list = []
    for tweet in db.saved_tweets_from_stream.find({"hour": {"$lte": current_hour}}).limit(2000):
        tweet_list.append({"loc": tweet["loc"], 
                            "text": tweet["text"], 
                            "score": tweet["score"], 
                            "id_str": tweet["id_str"], 
                            "screen_name": tweet["screen_name"],
                            "profile_img": tweet["profile_img"],
                            "hour": tweet["hour"],
                            "timestamp": tweet["timestamp"]
                            })
    return tweet_list

def get_tweets_by_hour(start_hour, end_hour):
    """Given the current date, a start hour, and an end hour, returns 
    list of all tweets from the current date between those hours.
    
    start_hour, end_hour: integers between 0 and 24
    """
    try:
        start_hour = int(start_hour)
        end_hour = int(end_hour)
    except:
        return []
    if not ((0 <= start_hour <= 24) and (0 <= end_hour <= 24)):
        return []
    else:
        tweet_list = []
        for tweet in db.saved_tweets_from_stream.find({"hour" : {"$gte": start_hour, 
                                                                "$lte": end_hour
                                                                }
                                                      }):     
            tweet_list.append({"loc": tweet["loc"], 
                                "text": tweet["text"],
                                "score": tweet["score"], 
                                "id_str": tweet["id_str"], 
                                "screen_name": tweet["screen_name"],
                                "profile_img": tweet["profile_img"],
                                "hour": tweet["hour"],
                                "timestamp": tweet["timestamp"]
                                })
        return tweet_list

def get_geocode(zipcode):
    """Given a valid zipcode, returns a string of 'latitiude, longitude, radius'.

    zipcode: a string of numbers with length 5
    """
    for document in db.zipcodes.find({"zipcode": zipcode}, {"lat": 1, "long": 1}):
        #this is the format twitter requires for the geocode search parameter
        geocode = str(document["lat"]) + ',' + str(document["long"]) + ',10mi'
        return geocode

def score_tweet_for_sentiment(data):
    token_list = clean_and_tokenize(data['text'])
    score = classifier.classify(best_word_features(token_list))
    data['score'] = score
    return data

def get_tweets_by_zipcode(zipcode):
    """Given a geocode string, returns a list of tweets from that zipcode via Twitter Search API, scored for sentiment.

    geocode: a string of 'latitiude, longitude, radius'
    """
    geocode = get_geocode(zipcode)
    tweet_list = []
    for page in Cursor(api.search, lang="en", count=50, geocode=geocode).pages(1):
        for tweet in page:
            data = {}
            #ensures the tweet has a geotag
            if tweet.coordinates:
                #ensures the geotag is within the USA
                if (-124 <= tweet.coordinates['coordinates'][0] <= -80) and (25 <= tweet.coordinates['coordinates'][1] <= 48):
                    data['loc'] = tweet.coordinates["coordinates"]
                    data['text'] = tweet.text
                    data['id_str'] = tweet.id_str
                    data['screen_name'] = tweet.user.screen_name
                    data['profile_img'] = tweet.user.profile_image_url_https
                    scored_tweet = score_tweet_for_sentiment(data)
                    tweet_list.append(scored_tweet)
    return tweet_list  

def clear_database():
    db.stream_tweets.remove({})
    return "cleared db"
