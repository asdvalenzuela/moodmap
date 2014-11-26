Happy California
===========

Happy California receives live, geotagged tweets and creates a real-time measurement of the sentiment balance in the Bay Area. Using natural language processing, sentiment analysis, and machine learning, the tweets are analyzed on the fly and mapped to browse and peruse. Feeling under the weather? Filter for happy tweets. Curious if people are more negative in the morning? Check out the hour-by-hour view. Not from the Bay Area? Enter your zipcode and see the current sentiment balance for your area.

### Technology

MongoDB, Leaflet/Mapbox, Pusher Websockets API, Scikit-learn, NLTK, Regex, Jquery, Javascript, Jquery UI, HTML, CSS, Flask, Python, Twitter API, Pickle

(Dependencies are listed in requirements.txt)

##### Sentiment Analysis

##### Database

##### Frontend

### Structure

#####(app.py)
Core of the flask app, lists all routes.

#####(model.py)
All database queries made by the flask app.

#####(analyzeTweets.py)
Core of the natural language processing and sentiment analysis. Used to build the Naïve Bayes classifier.

#####(SKanalyzeTweets.py)
Another version of analyzeTweets.py using Scikit-learn instead of NLTK.

#####(streamTweets.py)
Establishes connection to Twitter Stream API.

### References

http://help.sentiment140.com/for-students

http://www.laurentluce.com/posts/twitter-sentiment-analysis-using-python-and-nltk/ 

http://sentiment.christopherpotts.net/ 

http://streamhacker.com/2010/06/16/text-classification-sentiment-analysis-eliminate-low-information-features/