import model
import app
import unittest

class MyAppUnitTestCase(unittest.TestCase):

	def testGet_geocode(self):
		self.assertEqual(model.get_geocode('48640'), '43.605457,-84.27234,10mi')

	def testGet_todays_tweets(self):
		self.assertIs(type(model.get_todays_tweets(19, '11 22 14')), list)
		self.assertTrue(model.get_todays_tweets(19, '11 22 14')[0]['loc'])
		self.assertTrue(model.get_todays_tweets(19, '11 22 14')[0]['score'])
		self.assertTrue(model.get_todays_tweets(19, '11 22 14')[0]['id_str'])
		self.assertTrue(model.get_todays_tweets(19, '11 22 14')[0]['screen_name'])
		self.assertTrue(model.get_todays_tweets(19, '11 22 14')[0]['profile_img'])

	def testGet_tweets_by_hour(self):
		self.assertIs(type(model.get_tweets_by_hour('11 22 14', 0, 19)), list)
		self.assertTrue(model.get_tweets_by_hour('11 22 14', 0, 19)[0]['loc'])
		self.assertTrue(model.get_tweets_by_hour('11 22 14', 0, 19)[0]['score'])
		self.assertTrue(model.get_tweets_by_hour('11 22 14', 0, 19)[0]['id_str'])
		self.assertTrue(model.get_tweets_by_hour('11 22 14', 0, 19)[0]['screen_name'])
		self.assertTrue(model.get_tweets_by_hour('11 22 14', 0, 19)[0]['profile_img'])

	def testGet_tweets_by_zipcode(self):
		self.assertIs(type(model.get_tweets_by_zipcode('43.605457,-84.27234,10mi')), list)

	# def mockGetTweets(strt ,end): 
 #    	return["fake tweets"]

class MyAppIntegrationTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()
        # model.getTweets = mockGetTweets

    def tearDown(self):
    	pass

    def testHome(self):
    	result = self.app.get('/')
    	self.assertIn('<h2>Happy California: Sentiment of Live Tweets</h2>', result.data)

    def testZipcodeMap(self):
    	result = self.app.get('/zipcode_map')
    	self.assertIn('<h2>Find Tweets by Zipcode</h2>', result.data)


if __name__ == '__main__':
    unittest.main()