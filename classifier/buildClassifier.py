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

global best_words

def create_word_scores():
    tweets = get_tweets_from_db()
    postweets = tweets[800001:]
    negtweets = tweets[:800001]
 
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
    global best_words
    return dict([(word, True) for word in words if word in best_words])

def get_tweets_from_db():
    """Retrieves documents from database, returns the text of each tweet as a token list."""
    tweets = []
    for tweet in db.training.find({'polarity':'0'}):
        tweet_text = tweet["text"] 
        token_list = clean_and_tokenize(tweet_text)
        tweets.append((token_list, tweet["polarity"]))
    for tweet in db.training.find({'polarity':'4'}):
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

def main():
    global best_words
    tweets = get_tweets_from_db()
    tweet_list = tweets[1000:1599000]
    test_list = tweets[:1000]+ tweets[1599000:]
    word_scores = create_word_scores()
    best_words = find_best_words(word_scores, 500000)
    training_set = classify.apply_features(best_word_features, tweet_list)
    print "extracted features"
    # train the classifier with the training set
    classifier = NaiveBayesClassifier.train(training_set)
    print "trained classifier"
    # create the pickle file
    f = open('NBclassifier_new.pickle', 'wb')
    pickle.dump(classifier, f)
    f.close()
    print "created pickle"
    # test for precision and recall
    refsets = collections.defaultdict(set)
    testsets = collections.defaultdict(set)

    test_set = classify.apply_features(best_word_features, test_list)
 
    for i, (feats, label) in enumerate(test_set):
        refsets[label].add(i)
        observed = classifier.classify(feats)
        testsets[observed].add(i)
     
    print 'neg precision:', metrics.precision(refsets['0'], testsets['0'])
    print 'neg recall:', metrics.recall(refsets['0'], testsets['0'])
    print 'pos precision:', metrics.precision(refsets['4'], testsets['4'])
    print 'pos recall:', metrics.recall(refsets['4'], testsets['4'])
    # test_set = classify.apply_features(extract_features, test_list)
    # print "extracted features"
    print classify.accuracy(classifier, test_set)
    print classifier.show_most_informative_features(30)


if __name__ == ("__main__"):
    main()
