from pymongo import MongoClient
import os
import pickle
from analyzeTweets import best_word_features, clean_and_tokenize
import tweepy
from tweepy import OAuthHandler
from tweepy import Cursor 

# creates connection to db
client = MongoClient()
db = client.tweet_database

TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
# twitter OAuth process
auth = OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
# create api 
api = tweepy.API(auth)

f = open('NBclassifier.pickle', 'rb')
classifier = pickle.load(f)

def get_todays_tweets(current_hour, current_date):
    """Given the current date and hour, returns list of all tweets 
    from the current date up to the current hour.

    current_hour: integer between 0 and 24
    current date: string of 'month date year'
    """
    tweet_list = []
    for tweet in db.stream_tweets.find({"date": current_date, 
                                        "hour": {"$lte": current_hour}
                                        }):
        #ensures tweet has a geotag
        if "loc" in tweet:
            tweet_list.append({"loc": tweet["loc"], 
                                "text": tweet["text"], 
                                "score": tweet["score"], 
                                "id_str": tweet["id_str"], 
                                "screen_name": tweet["screen_name"],
                                "profile_img": tweet["profile_img"],
                                "date": tweet["date"],
                                "hour": tweet["hour"],
                                })
    return tweet_list

def get_tweets_by_hour(current_date, start_hour, end_hour):
    """Given the current date, a start hour, and an end hour, returns 
    list of all tweets from the current date between those hours.
    
    current_date: string of 'month date year'
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
        for tweet in db.stream_tweets.find({"date": current_date, 
                                            "hour" : {"$gte": start_hour, 
                                                      "$lte": end_hour}
                                            }):     
            #ensures tweet has a geotag   
            if "loc" in tweet:
                tweet_list.append({"loc": tweet["loc"], 
                                    "text": tweet["text"],
                                    "score": tweet["score"], 
                                    "id_str": tweet["id_str"], 
                                    "screen_name": tweet["screen_name"],
                                    "profile_img": tweet["profile_img"],
                                    "date": tweet["date"],
                                    "hour": tweet["hour"],
                                    })
        return tweet_list

def get_geocode(zipcode):
    """Given a valid zipcode, returns a string of 'latitiude, longitude, radius'.

    zipcode: a string with length 5
    """
    for document in db.zipcodes.find({"zipcode": zipcode}, {"lat": 1, "long": 1}):
        #this is the format twitter requires for the geocode search parameter
        geocode = str(document["lat"]) + ',' + str(document["long"]) + ',10mi'
        return geocode

def get_tweets_by_zipcode(geocode):
    """Given a geocode string, returns a list of tweets from that zipcode, scored for sentiment.

    geocode: a string of 'latitiude, longitude, radius'
    """
    tweet_list = []
    for page in Cursor(api.search, lang="en", count=100, geocode=geocode).pages(2):
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
                    #preprocess the tweet and score it for sentiment
                    token_list = clean_and_tokenize(data['text'])
                    score = classifier.classify(best_word_features(token_list))
                    data['score'] = score

                    tweet_list.append(data)
    return tweet_list  
