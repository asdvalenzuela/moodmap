from pymongo import MongoClient

# creates connection to db
client = MongoClient()
db = client.tweet_database

def get_tweets_from_db():
    """Retrieves documents from database and returns the coordinates of each tweet."""
    coordinate_list = []
    for tweet in db.search_tweetsNY.find().limit(1000):
        if "loc" in tweet:
            coordinate_list.append((tweet["loc"], tweet["text"].encode('utf8', 'ignore')))
    return coordinate_list

def update_geojson(coordinate_list):
    """Updates geojson file with coordinate list"""
    f = open("templates/point.geojson", "w")
    f.write('''{
  "type": "FeatureCollection",
  "features": [\n\t''')
    for coords in coordinate_list:
        f.write('''{
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          %s,
          %s
        ]
      },
      "properties": {
        "title": "%s",
        "marker-color": "#9c89cc",
        "marker-size": "medium",
        "marker-symbol": "building"
      }
    },\n\t''' % (coords[0][0], coords[0][1], coords[1]))
    f.write(']\n}')
    f.close()

coordinate_list = get_tweets_from_db()
update_geojson(coordinate_list)
