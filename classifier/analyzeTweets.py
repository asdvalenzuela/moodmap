from pymongo import MongoClient
from nltk import FreqDist, NaiveBayesClassifier, classify, BigramAssocMeasures, ConditionalFreqDist, metrics
import collections, itertools
import ChrisPottsTokenizer as CPT
import regExs as RE
import pickle

# creates connection to db
client = MongoClient()
db = client.tweet_database
training = db.training

# creates instance of tokenizer
t = CPT.Tokenizer()

global word_features

def create_word_scores():
    #reading pre-labeled input and splitting into lines
    tweets = get_tweets_from_db()
    postweets = tweets[5000:]
    negtweets = tweets[:5000]
 
    posWords = []
    negWords = []
    for tweet in postweets:
        posWords.append(tweet[0])
    for tweet in negtweets:
        negWords.append(tweet[0])

    posWords = list(itertools.chain(*posWords))
    negWords = list(itertools.chain(*negWords))

    word_fd = FreqDist()
    cond_word_fd = ConditionalFreqDist()

    for word in posWords:
        word_fd[word.lower()] += 1
        cond_word_fd['pos'][word.lower()] += 1
    for word in negWords:
        word_fd[word.lower()] += 1
        cond_word_fd['neg'][word.lower()] += 1

    pos_word_count = cond_word_fd['pos'].N()
    neg_word_count = cond_word_fd['neg'].N()
    total_word_count = pos_word_count + neg_word_count

    word_scores = {}
    for word, freq in word_fd.iteritems():
        pos_score = BigramAssocMeasures.chi_sq(cond_word_fd['pos'][word], (freq, pos_word_count), total_word_count)
        neg_score = BigramAssocMeasures.chi_sq(cond_word_fd['neg'][word], (freq, neg_word_count), total_word_count)
        word_scores[word] = pos_score + neg_score

    return word_scores

def find_best_words(word_scores, number):
    best_vals = sorted(word_scores.iteritems(), key=lambda (w, s): s, reverse=True)[:number]
    best_words = set([w for w, s in best_vals])
    return best_words

def best_word_features(words):
    best_words = find_best_words(create_word_scores(), 9000)
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
