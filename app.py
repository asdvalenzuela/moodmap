from flask import Flask, render_template, Response, request
import model
import json
import time

app = Flask(__name__)

current_date = time.strftime("%m %d %y") 
current_hour = time.strftime("%H")

@app.route('/')
def display_map():
    return render_template('map.html')

@app.route("/about")
def display_about():
    return render_template('about.html')

@app.route('/coordinates')
def return_coords():
    coordinate_list = model.get_tweets_from_db(current_hour, current_date)
    return Response(json.dumps(coordinate_list), mimetype='application/json')

@app.route("/get_tweets_by_time")
def get_tweets_by_date_range():
    start_time = request.args.get('startTime')    
    end_time = request.args.get('endTime')
    coordinate_list = model.get_tweets_by_time(current_date, start_time, end_time) 
    return Response(json.dumps(coordinate_list), mimetype='application/json')

if __name__ == "__main__":
    app.run(debug = True)