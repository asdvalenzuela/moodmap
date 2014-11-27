Happy California
===========

Happy California receives live, geotagged tweets and creates a real-time measurement of the sentiment balance in the Bay Area. Using natural language processing, sentiment analysis, and machine learning, the tweets are analyzed on the fly and mapped to browse and peruse. Feeling under the weather? Filter for happy tweets. Curious if people are more negative in the morning? Check out the hour-by-hour view. Not from the Bay Area? Enter your zipcode and see the current sentiment balance for your area.

![HappyTweetExample](https://raw.githubusercontent.com/asdvalenzuela/moodmap/master/static/img/HappyTweetExample.png)
![SadTweetExample](https://github.com/asdvalenzuela/moodmap/blob/master/static/img/SadTweetExample.png)

### Technology

MongoDB, Leaflet/Mapbox, Pusher Websockets API, Scikit-learn, NLTK, Regex, Jquery, Javascript, Jquery UI, HTML, CSS, Flask, Python, Twitter API, Pickle, Ajax

(Dependencies are listed in requirements.txt)

##### Sentiment Analysis
A training set of 1.6 million pre-labeled positive and negative tweets was used to train a Naïve Bayes classifier. The set was obtained from [Sentiment140](http://help.sentiment140.com/for-students). Each tweet was preprocessed to remove any usernames, links, and articles using regular expressions, then tokenized. The tokenization function preserved emoticons so that the presence or absence of positive or negative emotions could be used as a feature for the analysis. 

The final classifier was trained using only the 10,000 most useful features. To find the most informative features, a frequency distribution and conditional frequency distribution (conditions are positive and negative labels) were built. Each word was scored using a chi-square test, which compares the frequency of the word in each label to the frequency of the word in the whole dataset, and determines whether that difference is significant. After the words were scored, the top n most highly scored words were chosen. Each tweet was then checked for presence or absence of these top words. This process served to eliminate noise, or low-information features, in the dataset, which can decrease performance.

Many different features and combinations of features (ngrams, stopwords, stemming, different tokenization functions, etc.) were used to find the result with the most accuracy in predicting positive and negative tweets, and the highest precision and recalls scores across both labels. After training, the classifier was then serialized via the python module Pickle. The pickle file is then opened and the saved classifier used to determine the sentiment of incoming live tweets.

The classifier used in the current version of Happy California was created from analyzeTweets.py, which uses NLTK as the analytical library. I included SKanalyzeTweets.py to demonstrate the same process using Scikit-learn, and experiment with feature changes.

##### Database
The tweets used to train the classifier, the incoming tweets from the Twitter Stream API, and the location information for all U.S. zipcodes are stored in MongoDB. Mongo’s ability to store varied data in a JSON-like structure for easy storage and retrieval made it ideal for this use case.

##### Frontend

The front-end is composed of a Mapbox (built on Leaflet) map with custom markers and popups, custom CSS, and Jquery UI elements for the buttons and slider. Map interactivity is programmed with a combination of Jquery UI, Javascript, Jquery, Ajax, and Mapbox/Leaflet Javascript. Pusher Websocket API pushes the incoming tweets to Javascript, where they are mapped with Mapbox/Leaflet. 

![ViewByHour](https://github.com/asdvalenzuela/moodmap/blob/master/static/img/ViewByHourExample.png)
![TweetsByZipcode](https://github.com/asdvalenzuela/moodmap/blob/master/static/img/TweetsByZipcodeExample.png)

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

http://andybromberg.com/sentiment-analysis-python/
