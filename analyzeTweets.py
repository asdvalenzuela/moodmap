from nltk.classify import apply_features

training_set = [ "@rememberwhenCFV check me out please http://t.co/s7stHfOCn3  if you like it follow me and check out more http://t.co/4OuTqFHkEQ",
 			"@fowlduck might want to put a TW on that",
			"@Godschid312 plez!! TS song is all u need to know to know how MJ felt. Rightfully so, he killed MJ.",
			"3D scanning startup Fuel3D closes $6.4M Series A round http://t.co/RV22A5i3Xy",
			"RT @fitbit: Let today's workout become next month's warmup. #keepmoving",
			"Are white people turning Dia de los Muertos into a bummer?: http://t.co/IFU36JMQwF",
			"RT @BeardSpice: I'm good at reading lips and pretty much every other word there is",
			"RT @MooreHnter: Don't text me when you know I'm doing lines on my phone",
			"@TheBestTo_DoIt wat up bra",
			"Just posted a photo http://t.co/jOLsN6B5ul" ]

for item in training_set:
	#tokenize?

train_set = apply_features(text_features, ?)
test_set = apply_features(text_features, ?)

#what will be paseed to this function? an array of words? a string? one word at a time?
def text_features(?):
    features = {}
    features["first_letter"] = name[0].lower()
    features["last_letter"] = name[-1].lower()
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        features["count(%s)" % letter] = name.lower().count(letter)
        features["has(%s)" % letter] = (letter in name.lower())
    return features

