from pymongo import MongoClient
from nltk import FreqDist, NaiveBayesClassifier, classify
from nltk.classify import apply_features
import ChrisPottsTokenizer as CPT
from OpinionLexicon import positive_words, negative_words
import re
from emoticonCheck import *
from random import shuffle

# creates connection to db
client = MongoClient()
db = client.tweet_database
search_tweets = db.search_tweets

global word_features

username = r"""(@([A-Za-z0-9_]+))"""
username_re = re.compile(username, re.VERBOSE | re.I | re.UNICODE)

url = r"""((https?):((//)|(\\\\))+[\w\d:#@%/;$()~_?\+-=\\\.&]*)"""
url_re = re.compile(url, re.VERBOSE | re.I | re.UNICODE)

articles_pronouns = r"""(\s+)(a|an|and|the)(\s+)"""
articles_pronouns_re = re.compile(articles_pronouns, re.VERBOSE | re.I | re.UNICODE)

def get_pos_from_db():
    """Retrieves documents from database, preprocesses and returns the text of each tweet."""
    tweets = []
    for tweet in db.positive_tweets.find().limit(4600):
        tweet_text = tweet["text"]
        # remove retweets, usernames, and links from tweet
        if "RT" not in tweet_text:
            tweet_text = username_re.sub('', tweet_text)
            tweet_text = url_re.sub('', tweet_text)
            tweet_text = articles_pronouns_re.sub(' ', tweet_text)
            tweet_text = tweet_text.strip()
            token_list = t.tokenize(tweet_text)
            tweets.append((token_list, "positive"))

    shuffle(tweets)
    tweet_list = tweets[:2000]
    test_list = tweets[2000:]
    return [tweet_list, test_list]

def get_neg_from_db():
    """Retrieves documents from database, preprocesses and returns the text of each tweet."""
    tweet_list = []
    for tweet in db.negative_tweets.find().limit(4200):
        tweet_text = tweet["text"]
        # remove retweets, usernames, and links from tweet
        if "RT" not in tweet_text:
            tweet_text = username_re.sub('', tweet_text)
            tweet_text = url_re.sub('', tweet_text)
            tweet_text = articles_pronouns_re.sub(' ', tweet_text)
            tweet_text = tweet_text.strip()
            token_list = t.tokenize(tweet_text)
            tweet_list.append((token_list, "negative"))
    return tweet_list

def get_test_from_db():
    """Retrieves documents from database, preprocesses and returns the text of each tweet."""
    tweet_list = []
    for tweet in db.search_tweetsNY.find().limit(4000):
        tweet_text = tweet["text"]
        # remove retweets, usernames, and links from tweet
        if "RT" not in tweet_text:
            tweet_text = username_re.sub('', tweet_text)
            tweet_text = url_re.sub('', tweet_text)
            tweet_text = articles_pronouns_re.sub(' ', tweet_text)
            tweet_text = tweet_text.strip()
            token_list = t.tokenize(tweet_text)
            tweet_list.append((token_list))
    return tweet_list

t = CPT.Tokenizer()
# might want to remove URL before tokenizing

negation_list = ['never', 'no', 'nothing', 'nowhere', 'noone', 'none', 'not', 'haven\'t', 'havent', 'hasn\'t', 'hasnt', 
                'can\'t', 'cant', 'couldn\'t', 'couldnt', 'shouldn\'t', 'shouldnt', 'won\'t', 'wont', 'wouldn\'t', 'wouldnt', 
                'dont', 'doesnt', 'didnt', 'isnt', 'arent', 'aint', 'don\'t', 'doesn\'t', 'didn\'t', 'isn\'t', 'aren\'t', 'ain\'t']

punctuation_list = ['.', ':', ';', '!', '?']

def negation_marking(token_list):
    """Append a _NEG suffix to every word between a negation and a punctuation mark."""
    neg = False
    for index in range(len(token_list)):
        if token_list[index] in negation_list:
            neg = True
        elif token_list[index] in punctuation_list:
            neg = False 
        elif neg:
            token_list[index] += "_NEG"
    return token_list

def create_training_set(tweet_list):
    """Creates a list of tuples ([tokens], 'label') The label is based on the amount of words in the tweet marked as positive or negative"""
    train_set = []
    for item in tweet_list:
        token_list = t.tokenize(item)
        # token_list = negation_marking(token_list)
        #this will turn into the feature extraction function
        # score = 0
        # for token in token_list:
        #     if token in positive_words:
        #         score += 1
        #     if token in negative_words:
        #         score -= 1
        #     if has_pos_emoticon(token):
        #         score += 2
        #     if has_neg_emoticon(token):
        #         score -= 2
        # if score > 0:
        train_set.append((token_list, 'positive'))
        # if score < 0:
        #     train_set.append((token_list, 'negative'))
    return train_set

def get_words_in_tweets(train_set):
    """Returns list of all unique words in all tweets"""
    all_words = []
    for (words, sentiment) in train_set:
      all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    """Creates a frequency distribution so that words that occur more times in the set are weighted"""
    wordlist = FreqDist(wordlist)
    #throw out here, then check where the words are , optimization problem
    word_features = wordlist.keys()
    return word_features

def extract_features(tweet):
    global word_features
    document_words = set(tweet)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

def main():
    global word_features
    tweet_list, test_list = get_pos_from_db()
    tweet_list2 = get_neg_from_db()
    tweet_list = tweet_list + tweet_list2
    # train_set = create_training_set(tweet_list)
    word_features = get_word_features(get_words_in_tweets(tweet_list))
    # creates list of tuples, each tuple consists of a dictionary of features and a label
    training_set = apply_features(extract_features, tweet_list)
    # train the classifier with the training set
    classifier = NaiveBayesClassifier.train(training_set)
    
    # now test the classifier on tweets from NYC
    # test_list = get_test_from_db()
    # this is essentially a map
    test_set = apply_features(extract_features, test_list)
    print classify.accuracy(classifier, test_set)
    print classifier.show_most_informative_features(30)
    print classifier.classify(extract_features(["thank", "you", "for", "the", "help", "you're", 'the', 'best']))
    print classifier.classify(extract_features(["Im", 'so', 'happy', 'this', 'is', 'great']))
    print classifier.classify(extract_features(['You\'re', 'the', 'worst']))
    print classifier.classify(extract_features(['I', 'hate', 'you']))


    # errors = []
    # for (text, label) in test_set:
    #     guess = classifier.classify(extract_features(text))
    #     if guess != label:
    #         errors.append( (label, guess, text) )
    # print errors




if __name__ == ("__main__"):
    main()

# feature_list = []
#   for token in neg_token_list:
#       if token in positive_words:
#           feature_list.append((token, True))
#       if token in negative_words:
#           feature_list.append((token, False))
#   tweet_dict[item] = feature_list
