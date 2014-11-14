from pymongo import MongoClient

# creates connection to db
client = MongoClient()
db = client.tweet_database

def get_tweets_from_db():
    """Retrieves documents from database and returns the coordinates of each tweet."""
    coordinate_list = []
    for tweet in db.stream_tweets.find({"score": {"$nin": ["0","4"]}}):
        if "loc" in tweet:
            coordinate_list.append({"long_": tweet["loc"][0], "lat_": tweet["loc"][1], 
                                    "text": tweet["text"], "id_str": tweet["id_str"] })
    return coordinate_list

def update_doc(id_str, score):
    db.stream_tweets.update({'id_str': id_str}, {"$set": {"score": score}})