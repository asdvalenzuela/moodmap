from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

@app.route("/")
def display_map():
	return render_template("map.html")

@app.route("/geojson")
def geojson():
	geojson = json.loads(open("templates/point.geojson").read())
	return jsonify(geojson)

@app.route("/test")
def test():
	lat_ = 1
	long_ = 1
	title = "Yay"
	features = [
    	{ "type": "Feature",
    		"geometry": {
    			"type": "Point",
    			"coordinates": [lat_, long_]
    		},
    		"properties": {
    		  "title": title,
    		  "marker-color": "#333",
    		  "marker-size" :"medium",
    		  "marker-symbol": "building"
    		}
    	}
    ]
	new_pts = {
    	"type": "FeatureCollection",
    	"features": [ features ]
    }


	return json.dumps(new_pts)

	# geojson = json.loads(open("templates/point2.geojson").read())
	# return jsonify(geojson)

if __name__ == "__main__":
	app.run(debug = True)