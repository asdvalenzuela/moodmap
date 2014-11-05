from nltk.classify import apply_features
import ChrisPottsTokenizer as CPT
from OpinionLexicon import positive_words, negative_words

training_set = [ 
			"Are white people turning Dia de los Muertos into a bummer?: http://t.co/IFU36JMQwF",
			"Just posted a photo http://t.co/jOLsN6B5ul",
			"RT @shots: @JBCrewdotcom glad you had a great bday!",
			"Client testimonial submitted on 9/13/2014: Thanks very much for this wonderful editing. The text has been improved clearly!",
			"@allayva Hey! That's not the attitude to have! :) You can also sign up for tours by the way!",
			"@rtrouton I'm worried someone is going to come by and just steal our building.",
			"Sunset Overdrive is so good. I love it. Best thing Insomniac has ever made. Smart, stylish, witty, funny, fun, with great comb",
			"I don't think I will enjoy it: it might be too spicy."
			]

t = CPT.Tokenizer()
# might want to remove URL before tokenizing

negation_list = ['never', 'no', 'nothing', 'nowhere', 'noone', 'none', 'not', 'haven\'t', 'havent', 'hasn\'t', 'hasnt', 
				'can\'t', 'cant', 'couldn\'t', 'couldnt', 'shouldn\'t', 'shouldnt', 'won\'t', 'wont', 'wouldn\'t', 'wouldnt', 
				'dont', 'doesnt', 'didnt', 'isnt', 'arent', 'aint', 'don\'t', 'doesn\'t', 'didn\'t', 'isn\'t', 'aren\'t', 'ain\'t']

punctuation_list = ['.', ':', ';', '!', '?']

def negation_marking(token_list):
	"""Append a _NEG suffix to every word between a negation and a punctuation mark."""
	next_index = 1
	for index in range(len(token_list)):
		if token_list[index] in negation_list:
			while token_list[index + next_index] not in punctuation_list: 
				token_list[index+next_index] += '_NEG'
				next_index += 1
	return token_list	

token_list = t.tokenize(training_set[-1])
neg_token_list = negation_marking(token_list)
feature_list = []
for token in neg_token_list:
	if token in positive_words:
		feature_list.append((token, True))
	if token in negative_words:
		feature_list.append((token, False))
print feature_list


#identify semantic groupings and relationships that are relevant for sentiment
	#apply negation
#function to tokenize each tweet

# train_set = apply_features(text_features, ?)
# test_set = apply_features(text_features, ?)

# #what will be paseed to this function? an array of words? a string? one word at a time?
# def text_features(?):
#     features = {}
#     features["first_letter"] = name[0].lower()
#     features["last_letter"] = name[-1].lower()
#     for letter in 'abcdefghijklmnopqrstuvwxyz':
#         features["count(%s)" % letter] = name.lower().count(letter)
#         features["has(%s)" % letter] = (letter in name.lower())
#     return features

# classifier = nltk.NaiveBayesClassifier.train(train_set)

# print classifier.classify(text_features(tweet1))
# print classifier.classify(gender_features(tweet2))
# print nltk.classify.accuracy(classifier, test_set)


