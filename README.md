Happy California
===========

Happy California receives live, geotagged tweets and creates a real-time measurement of the sentiment balance in the Bay Area. Using natural language processing, sentiment analysis, and machine learning, the tweets are analyzed on the fly and mapped to browse and peruse. Feeling under the weather? Filter for happy tweets. Curious if people are more negative in the morning? Check out the hour-by-hour view. Not from the Bay Area? Enter your zipcode and see the current sentiment balance for your area.

### Technology

MongoDB, Leaflet/Mapbox, Pusher Websockets API, Scikit-learn, NLTK, Regex, Jquery, Javascript, Jquery UI, HTML, CSS, Flask, Python, Twitter API, Pickle

(Dependencies are listed in requirements.txt)

##### Sentiment Analysis
A training set of 1.6 million pre-labeled positive and negative tweets was used to train a Naïve Bayes classifier. The set was obtained from Sentiment140 and can be found in the references section. 

Each tweet in the training set was preprocessed to remove any usernames, links, and articles (the, a, and, the, etc.) included in the text, then tokenized. The tokenization process I used preserved emoticons so that the presence and absence of positive or negative emotions could be used as a feature for the analysis.

![alt tag](https://raw.githubusercontent.com/asdvalenzuela/moodmap/master/static/img/machine_learning_process.png)

The classifier is then serialized via the python module Pickle, which is then opened and used to classify the incoming live tweets for positive or negative sentiment.

Though the classifier used in the final product was created from analyzeTweets.py, which uses NLTK as the analytical library, I included SKanalyzeTweets.py to demonstrate the same process using Scikit-learn.

##### Database
The tweets used to train the classifier, the incoming tweets, and the location information for all U.S. zipcodes are stored in MongoDB. Mongo’s ability to store different types of information in a Json-like structure for easy storage and retrieval made it ideal for this use case.

##### Frontend
The frontend receives the tweet, checks if the tweet is positive or negative, and maps the tweet with the appropriate emoticon using Leaflet/Mapbox. The user is then able to click on each mapped emoticon to view the contents of the tweet, including the screenname, profile image, and tweet text. In addition, the user is able to click on the control buttons on to view only positive tweets, only negative tweets, all tweets, or clear the entire map if it’s getting too crowded.

When the page first loads, the frontend detects the current hour of the day and loads all tweets from 12 am that day to the present hour. The user can then adjust the slider to view tweets by a different hour range.

On the Search by Zipcodes page, the user can enter their zipcode to see tweets analyzed by sentiment from that area. These tweets are from the Twitter search api, and while very recent are not real-time.

### Structure

#####app.py
Core of the flask app, lists all routes.

#####model.py
All database queries made by the flask app.

#####analyzeTweets.py
Core of the natural language processing and sentiment analysis. Used to build the Naïve Bayes classifier.

#####SKanalyzeTweets.py
Another version of analyzeTweets.py using Scikit-learn instead of NLTK.

#####streamTweets.py
Establishes connection to Twitter Stream API.

### References

http://help.sentiment140.com/for-students

http://www.laurentluce.com/posts/twitter-sentiment-analysis-using-python-and-nltk/ 

http://sentiment.christopherpotts.net/ 

http://streamhacker.com/2010/06/16/text-classification-sentiment-analysis-eliminate-low-information-features/
