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
    return Response(json.dumps(coordinate_list), mimetype='application/json')

if __name__ == "__main__":
    app.run(debug = True)