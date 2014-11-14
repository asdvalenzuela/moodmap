from flask import Flask, render_template, Response
import model
import json
import pickle
from analyzeTweetsClean import best_word_features, clean_and_tokenize



app = Flask(__name__)

@app.route('/')
def display_map():
    return render_template('map.html')

@app.route('/coordinates')
def return_coords():
    f = open('NBclassifier.pickle', 'rb')
    classifier = pickle.load(f)
    coordinate_list = model.get_tweets_from_db()
    for tweet in coordinate_list:
        if 'score' not in tweet:
            tweet_text = tweet['text']
            token_list = clean_and_tokenize(tweet_text)
            score = classifier.classify(best_word_features(token_list))
            tweet['score'] = score
            model.update_doc(tweet['id_str'], tweet['score'])
    f.close()
    return Response(json.dumps(coordinate_list), mimetype='application/json')

if __name__ == "__main__":
    app.run(debug = True)