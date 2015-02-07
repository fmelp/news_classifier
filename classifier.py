#!/bin/python

import string
import sys
import random
import operator
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction import DictVectorizer
from sklearn.cross_validation import train_test_split

keyWords = ["shooting", "firearm", "gun", "pistol", "bullet", "gunshot"]

#read in raw data from file and return a list of (label, article) tuples
def get_data(filename): 
	data = [line.strip().split('\t') for line in open(filename).readlines()]
	random.shuffle(data)
	return data


def remove_stop_word(lol):
	stop_words = [line.strip() for line in open('stopwords.txt')]
	for word in stop_words:
		if word in ['.', ',', '/', ';', '!', '?', '-', "\\"]:
			lol[0] = lol[0].replace(word, ' ')
		if len(word) <= 4:
			lol = [x for x in lol if x not in stop_words]
		else:
			lol[0] = lol[0].replace(word, '')
	return lol


def get_features(X) :
	features = []
	stop_words = [line.strip() for line in open('stopwords.txt')]

	for x in X:
		f ={}
		article = x.split()
		article = [word for word in article if word not in stop_words]
		for word in article:
			if word in f : f[word] += 1
			else : f[word] = 1
		features.append(f)
	return features



#vectorize feature dictionaries and return feature and label matricies
def get_matricies(data) : 
	dv = DictVectorizer(sparse=True) 
	le = LabelEncoder()
	y = [d[0] for d in data]
	texts = [d[1] for d in data]
	X = get_features(texts)
	#Here we are returning 5 things, the label vector y and feature matrix X, but also the texts from which the features were extracted and the 
	#objects that were used to encode them. These will come in handy for your analysis, but you can ignore them for the initial parts of the assignment
	return le.fit_transform(y), dv.fit_transform(X), texts, dv, le


#train and multinomial naive bayes classifier
def train_classifier(X, y):
	clf = LogisticRegression()
	clf.fit(X,y)
	return clf


#test the classifier
def test_classifier(clf, X, y):
	return clf.score(X,y)


#cross validation	
def cross_validate(X, y, numfolds=5):
	test_accs = []
	split = 1.0 / numfolds
	for i in range(numfolds):
		x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=split, random_state=i)
		clf = train_classifier(x_train, y_train)
		test_acc = test_classifier(clf, x_test, y_test)
		test_accs.append(test_acc)
		print 'Fold %d : %.05f'%(i,test_acc)
	test_average = float(sum(test_accs))/ numfolds
	print 'Test Average : %.05f'%(test_average)
	print
	return test_average


#run a rule based classifier and calculate the accuracy
def rule_based_classifier(data):
	correct = 0.0; total = 0.0
	for label, text in data : 
		prediction = '0'
		for keyWord in keyWords:
			if keyWord in text:
				prediction = '1'
		if prediction == label:
			correct += 1
		total += 1
	print 'Rule-based classifier accuracy: %.05f'%(correct / total)


#train and multinomial naive bayes classifier
def get_top_features(X, y, dv):
	clf = train_classifier(X, y)
	#the DictVectorizer object remembers which column number corresponds to which feature, and return the feature names in the correct order
	feature_names = dv.get_feature_names()
	weights_ls = clf.coef_
	d = {}
	for keyWord in keyWords:
		d[keyWord] = weights_ls[0][feature_names.index(keyWord)]
	
	return d
	

def get_misclassified_examples(y, X, texts) :
	x_train, x_test, y_train, y_test, train_texts, test_texts = train_test_split(X, y, texts)
	clf = train_classifier(x_train, y_train)
	pred = clf.predict(x_test)
	preds_bool = []	
	false_pos = ''
	for i in range(len(y_test)):
		if pred[i] == y_test[i]:
			preds_bool.append(True)
		else:
			preds_bool.append(False)
			if pred[i] == 1:
				false_pos = test_texts[i]
			
	print "\nFALSE POSITIVE EXAMPLES: " + false_pos
	return preds_bool


if __name__ == '__main__' : 

	raw_data = get_data('articles')
	
	print '\nRule-based classification'
	rule_based_classifier(raw_data)

	print '\nStatistical classification'
	y, X, texts, dv, le = get_matricies(raw_data)
	cross_validate(X,y)	

	top_features = get_top_features(X, y, dv)
	print '\nTop Features: '
	print top_features
	get_misclassified_examples(y, X, texts)

