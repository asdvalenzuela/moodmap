from flask import Flask, render_template, Response, request
import model
import json
import time

app = Flask(__name__)

current_date = time.strftime("%m %d %y") 
current_hour = int(time.strftime("%H"))

@app.route('/')
def display_map():
    return render_template('map.html')

@app.route('/coordinates')
def return_coords():
    """Returns list of all tweets from the current date up to the current hour.
    
    current_date: string of 'month date year'
    current_hour: integer between 0 and 24
    """
    tweet_list = model.get_todays_tweets(current_hour, current_date)
    return Response(json.dumps(tweet_list), mimetype='application/json')

@app.route("/get_tweets_by_time")
def get_tweets_by_time_range():
    """Takes start hour and end hour from frontend, returns list of all tweets 
    from the current date between those hours.
    
    current_date: string of 'month date year'
    start_hour, end_hour: integers between 0 and 24
    """
    start_hour = int(request.args.get('startTime'))    
    end_hour = int(request.args.get('endTime'))
    tweet_list = model.get_tweets_by_hour(current_date, start_hour, end_hour) 
    return Response(json.dumps(tweet_list), mimetype='application/json')

@app.route("/zipcode_map")
def display_zipcode_map():
    return render_template('zipcode_map.html')

@app.route("/get_tweets_by_zipcode")
def get_tweets_by_zipcode():
    """Takes zipcode from frontend, returns a list of tweets from that zipcode.

    zipcode: a string with length 5
    """
    # if len(zipcode) != 5:
    #     return Response("[]")

    zipcode = request.args.get('zipcode')
    geocode = model.get_geocode(zipcode)
    tweet_list = model.get_tweets_by_zipcode(geocode)
    return Response(json.dumps(tweet_list), mimetype='application/json')

if __name__ == "__main__":
    app.run(debug = True)