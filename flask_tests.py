import model
import app
import unittest

class MyAppUnitTestCase(unittest.TestCase):

	def testGet_geocode(self):
		self.assertEqual(model.get_geocode('48640'), '43.605457,-84.27234,10mi')

	def testGet_todays_tweets(self):
		#tests if tweets are from the correct date, that the correct type is returned, 
		#and the dictionary contains the correct keys
		self.assertIs(type(model.get_todays_tweets(19, '11 22 14')), list)
		data = model.get_todays_tweets(19, '11 22 14')
		for index in range(len(data)):
			self.assertEqual(data[index]['date'], '11 22 14')
			self.assertTrue('loc' in data[index])
			self.assertTrue(data[index]['score'])
			self.assertTrue(data[index]['id_str'])
			self.assertTrue(data[index]['screen_name'])
			self.assertTrue(data[index]['profile_img'])

	def testGet_tweets_by_hour(self):
		#tests if tweets are from the correct date, that the correct type is returned, 
		#and the dictionary contains the correct keys
		self.assertIs(type(model.get_tweets_by_hour('11 22 14', 0, 19)), list)
		data = model.get_tweets_by_hour('11 22 14', 0, 19)
		for index in range(len(data)):
			self.assertEqual(data[index]['date'], '11 22 14')
			self.assertTrue(data[index]['loc'])
			self.assertTrue(data[index]['score'])
			self.assertTrue(data[index]['id_str'])
			self.assertTrue(data[index]['screen_name'])
			self.assertTrue(data[index]['profile_img'])

		#test for string values for start_hour and end_hour
		data = model.get_tweets_by_hour('11 22 14', '0', '19')
		self.assertIs(type(data), list)
		self.assertTrue(len(data) > 0)

		#test for invalid start and end times
		data = model.get_tweets_by_hour('11 22 14', 'a', 'foo')
		self.assertIs(type(data), list)
		self.assertTrue(len(data) == 0)
		data = model.get_tweets_by_hour('11 22 14', '-1', '50')
		self.assertIs(type(data), list)
		self.assertTrue(len(data)== 0)
		

	# def testGet_tweets_by_zipcode(self):
	# 	self.assertIs(type(model.get_tweets_by_zipcode('43.605457,-84.27234,10mi')), list)


class MyAppIntegrationTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()

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