from flask import Flask, render_template, Response, request, redirect
import model
import json
import time
import os

app = Flask(__name__)

def get_current_hour():
    """Returns current hour for use in db queries."""
    return int(time.strftime("%H"))

@app.route('/')
def display_map():
    return render_template('map.html')

@app.route('/todays_tweets')
def todays_tweets():
    """Returns list of all tweets from the current date up to the current hour.
    
    current_hour: integer between 0 and 24
    """
    current_hour = get_current_hour()
    tweet_list = model.get_todays_tweets(current_hour)
    return Response(json.dumps(tweet_list), mimetype='application/json')

@app.route('/tweets_by_hour')
def tweets_by_hour():
    """Takes start hour and end hour from frontend, returns list of all tweets 
    from the current date between those hours.
    
    start_hour, end_hour: integers between 0 and 24
    """
    start_hour = request.args.get('startTime')
    end_hour = request.args.get('endTime')
    tweet_list = model.get_tweets_by_hour(start_hour, end_hour) 
    if len(tweet_list) == 0:
        return "Please check your start and end times."
    else:
        return Response(json.dumps(tweet_list), mimetype='application/json')

@app.route("/zipcode_map")
def display_zipcode_map():
    return render_template('zipcode_map.html')

@app.route("/get_tweets_by_zipcode")
def get_tweets_by_zipcode():
    """Takes zipcode from frontend, returns a list of tweets from that zipcode.

    zipcode: a string of numbers with length 5
    """
    zipcode = request.args.get('zipcode')
    tweet_list = model.get_tweets_by_zipcode(zipcode)
    return Response(json.dumps(tweet_list), mimetype='application/json')

@app.route("/clear_db")
def clear_db():
    """Clear database of previous day's tweets"""
    model.clear_database()
    return redirect("/")

if __name__ == "__main__":
    DEBUG = "NO_DEBUG" not in os.environ
    app.run(debug = DEBUG)