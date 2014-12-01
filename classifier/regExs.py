import re

#remove username from tweet
username = r"""(@([A-Za-z0-9_]+))"""
username_re = re.compile(username, re.VERBOSE | re.I | re.UNICODE)

#remove url from tweet
url = r"""((https?):((//)|(\\\\))+[\w\d:#@%/;$()~_?\+-=\\\.&]*)"""
url_re = re.compile(url, re.VERBOSE | re.I | re.UNICODE)

#remove articles from tweet
articles = r"""(\s+)(a|an|and|the)(\s+)"""
articles_re = re.compile(articles, re.VERBOSE | re.I | re.UNICODE)

#check for positive emoticons
positive_emoticon_string = r"""
    (?:
      [<>]?
      [:;=8]                     # eyes
      [\-o\*\']?                 # optional nose
      [\)\]dDpP] 				         # mouth      
      |
      [\)\]dDpP] 				         # mouth
      [\-o\*\']?                 # optional nose
      [:;=8]                     # eyes
      [<>]?
    )"""

#check for negative emoticons
negative_emoticon_string = r"""
    (?:
      [<>]?
      [:;=8]                     # eyes
      [\-o\*\']?                 # optional nose
      [\(\[/\:\}\{@\|\\] 		     # mouth      
      |
      [\(\[/\:\}\{@\|\\]		     # mouth
      [\-o\*\']?                 # optional nose
      [:;=8]                     # eyes
      [<>]?
    )"""

pos_emoticon_re = re.compile(positive_emoticon_string, re.VERBOSE | re.I | re.UNICODE)
neg_emoticon_re = re.compile(negative_emoticon_string, re.VERBOSE | re.I | re.UNICODE)

def has_pos_emoticon(tweet):
    pos_emoticon = pos_emoticon_re.search(tweet)
    if pos_emoticon:
    	return True
    else:
    	return False

def has_neg_emoticon(tweet):
    neg_emoticon = neg_emoticon_re.search(tweet)
    if neg_emoticon:
    	return True
    else:
    	return False


