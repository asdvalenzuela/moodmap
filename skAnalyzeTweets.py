import numpy as np
import regExs as RE
from pymongo import MongoClient
import ChrisPottsTokenizer as CPT
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn import cross_validation
from sklearn import metrics

client = MongoClient()
db = client.tweet_database
training = db.training

t = CPT.Tokenizer()

def clean_and_tokenize(tweet):
    tweet = RE.username_re.sub('', tweet)
    tweet = RE.url_re.sub('', tweet)
    tweet = RE.articles_re.sub(' ', tweet)
    tweet = tweet.strip()
    return tweet

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

def get_tweets_from_db():
    """Retrieves documents from database, returns list of tuples (text of each tweet as a token list, polarity)."""
    labels = []
    documents = []
    for tweet in db.training.find({'polarity':'0'}).limit(5000):
        tweet_text = tweet["text"] 
        labels.append(tweet["polarity"])
        documents.append(tweet_text)
    for tweet in db.training.find({'polarity':'4'}).limit(5000):
        tweet_text = tweet["text"]
        labels.append(tweet["polarity"])
        documents.append(tweet_text) 
    return [labels, documents]

labels, documents = get_tweets_from_db()
vectorizer = TfidfVectorizer(tokenizer=t.tokenize, preprocessor=clean_and_tokenize)

X = vectorizer.fit_transform(documents)
y = np.array(labels)

clf = BernoulliNB()
cv = cross_validation.StratifiedKFold(y,5)

precision_pos=[]
recall_pos=[]
precision_neg=[]
recall_neg=[]
for train, test in cv:
    X_train = X[train]
    X_test = X[test]
    y_train = y[train]
    y_test = y[test]
    clf.fit(X_train, y_train)
    y_hat = clf.predict(X_test)
    p,r,_,_ = metrics.precision_recall_fscore_support(y_test, y_hat)
    precision_pos.append(p[1])
    recall_pos.append(r[1])
    precision_neg.append(p[0])
    recall_neg.append(r[0])


print 'precision pos:',np.average(precision_pos), '+/-', np.std(precision_pos)
print 'recall pos:', np.average(recall_pos), '+/-', np.std(recall_pos)
print 'precision neg:',np.average(precision_neg), '+/-', np.std(precision_neg)
print 'recall neg:', np.average(recall_neg), '+/-', np.std(recall_neg)

neg_sample = "I am so upset today. I hate life."
neg_sample = vectorizer.transform([neg_sample])
print clf.predict(neg_sample)
pos_sample = "I love everyone! So cool!"
pos_sample = vectorizer.transform([pos_sample])
print clf.predict(pos_sample)

probs=clf.feature_log_prob_[1]
len(probs)
features=vectorizer.get_feature_names()
len(features)
print sorted(zip(probs,features), reverse=True)[:30]



