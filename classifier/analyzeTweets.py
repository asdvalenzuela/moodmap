from pymongo import MongoClient
from nltk import FreqDist, NaiveBayesClassifier, classify, BigramAssocMeasures, ConditionalFreqDist, metrics
import collections, itertools
import ChrisPottsTokenizer as CPT
import regExs as RE
import pickle

global best_words

f = open('classifier/bestwords.pickle', 'rb')
best_words = pickle.load(f)

# creates connection to db
client = MongoClient()
db = client.tweet_database
training = db.training

# creates instance of tokenizer
t = CPT.Tokenizer()


def best_word_features(words):
    global best_words
    return dict([(word, True) for word in words if word in best_words])

def get_tweets_from_db():
    """Retrieves documents from database, returns the text of each tweet as a token list."""
    tweets = []
    for tweet in db.training.find({'polarity':'0'}).limit(5000):
        tweet_text = tweet["text"] 
        token_list = clean_and_tokenize(tweet_text)
        tweets.append((token_list, tweet["polarity"]))
    for tweet in db.training.find({'polarity':'4'}).limit(5000):
        tweet_text = tweet["text"]
        token_list = clean_and_tokenize(tweet_text)
        tweets.append((token_list, tweet["polarity"]))     
    return tweets

def clean_and_tokenize(tweet):
    tweet = RE.username_re.sub('', tweet)
    tweet = RE.url_re.sub('', tweet)
    tweet = RE.articles_re.sub(' ', tweet)
    tweet = tweet.strip()
    token_list = t.tokenize(tweet)
    return token_list
