from flask import Flask, render_template, Response, jsonify
import model
import json

app = Flask(__name__)

@app.route('/')
def display_map():
    return render_template('map.html')

@app.route('/coordinates')
def return_coords():
    coordinate_list = model.get_tweets_from_db()
    print len(coordinate_list)
    tweet = coordinate_list[0]
    model.update_doc(tweet['id_str'])
    print "finished"
    return jsonify(tweet)

if __name__ == "__main__":
    app.run(debug = True)