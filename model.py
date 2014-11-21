from pymongo import MongoClient

# creates connection to db
client = MongoClient()
db = client.tweet_database

def get_tweets_from_db(current_hour, current_date):
    """Retrieves documents from database and returns the coordinates of each tweet."""
    coordinate_list = []
    for tweet in db.stream_tweets.find({"date": current_date, "hour": {"$lte": current_hour}}):
        if "loc" in tweet:
            coordinate_list.append({"loc": tweet["loc"], "text": tweet["text"], "score": tweet["score"], "id_str": tweet["id_str"]})
    return coordinate_list

def get_tweets_by_time(current_date, start_time, end_time):
    coordinate_list = []
    for tweet in db.stream_tweets.find({"date": current_date, "hour" : {"$gte": start_time, "$lte": end_time}}):        
        if "loc" in tweet:
            coordinate_list.append({"loc": tweet["loc"], "text": tweet["text"], "score": tweet["score"], "id_str": tweet["id_str"]})
    return coordinate_list