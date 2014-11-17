from pymongo import MongoClient
from nltk import FreqDist, NaiveBayesClassifier, classify, metrics
import ChrisPottsTokenizer as CPT
import regExs as RE
import collections
import re, math, collections, itertools
import nltk, nltk.classify.util, nltk.metrics
from nltk.classify import NaiveBayesClassifier
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist
import pickle


# creates connection to db
client = MongoClient()
db = client.tweet_database
training = db.training
NY = db.search_tweetsNY

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
    #http://stackoverflow.com/questions/367155/splitting-a-string-into-words-and-punctuation
    #breaks up the sentences into lists of individual words (as selected by the input mechanism) and appends 'pos' or 'neg' after each list
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

def extract_features(tweet):
    """"""
    global word_features
    document_words = set(tweet)
    features = {}
    token_list = negation_marking(tweet)
    for token in token_list:
        if RE.has_pos_emoticon(token):
            features['pos_emoticon'] = True
        if RE.has_neg_emoticon(token):
            features['neg_emoticon'] = True
    for word in word_features:
        features[word] = (word in document_words)
    return features

def get_words_in_tweets(train_set):
    """Returns list of all words in all tweets"""
    all_words = []
    for (words, sentiment) in train_set:
      all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    """Creates a frequency distribution so that words that occur more times in the set are weighted"""
    wordlist = FreqDist(wordlist)
    print wordlist 
    print wordlist.most_common(50)
    raw_input()
    word_features = wordlist.keys()
    return word_features

def main():

    #(0 = negative, 2 = neutral, 4 = positive)
    global word_features
    tweets = get_tweets_from_db()
    tweet_list = tweets[1000:9000]
    test_list = tweets[:1000]+ tweets[9000:]
    # word_features = get_word_features(get_words_in_tweets(tweet_list))
    # creates list of tuples, each tuple consists of a dictionary of features and a label
    training_set = classify.apply_features(best_word_features, tweet_list)
    print "extracted features"
    # train the classifier with the training set
    classifier = NaiveBayesClassifier.train(training_set)
    print "trained classifier"
    f = open('NBclassifier.pickle', 'wb')
    pickle.dump(classifier, f)
    f.close()
    # refsets = collections.defaultdict(set)
    # testsets = collections.defaultdict(set)

    # test_set = classify.apply_features(best_word_features, test_list)
 
    # for i, (feats, label) in enumerate(test_set):
    #     refsets[label].add(i)
    #     observed = classifier.classify(feats)
    #     testsets[observed].add(i)
     
    # print 'neg precision:', metrics.precision(refsets['0'], testsets['0'])
    # print 'neg recall:', metrics.recall(refsets['0'], testsets['0'])
    # print 'pos precision:', metrics.precision(refsets['4'], testsets['4'])
    # print 'pos recall:', metrics.recall(refsets['4'], testsets['4'])
    # # test_set = classify.apply_features(extract_features, test_list)
    # # print "extracted features"
    # print classify.accuracy(classifier, test_set)
    # print classifier.show_most_informative_features(30)
    # print classifier.classify(extract_features(["thank", "you", "for", "the", "help", "you're", 'the', 'best']))
    # print classifier.classify(extract_features(["Im", 'so', 'happy', 'this', 'is', 'great']))
    # print classifier.classify(extract_features(['You\'re', 'the', 'worst']))
    # print classifier.classify(extract_features(['I', 'hate', 'you']))


if __name__ == ("__main__"):
    main()
