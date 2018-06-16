import numpy as np
import os

path_pos = "/Users/rafa/Downloads/review_polarity/txt_sentoken/pos/"
path_neg = "/Users/rafa/Downloads/review_polarity/txt_sentoken/neg/"
positive_vectors=[]
negative_vectors=[]
words = ["awful","bad","boring","dull","effective","enjoyable","great","hilarious"]

i=0
for pos_reviews_file in os.listdir(path_pos):
	pos_review = open(path_pos+pos_reviews_file, "r")
	vector = [0,0,0,0,0,0,0,0]
	positive_vectors.append(vector)
	for line in pos_review:
		for word in line.split():
			if word.lower() == "awful":
				positive_vectors[i][0] = 1
			elif word.lower() == "bad":
				positive_vectors[i][1] = 1
			elif word.lower() == "boring":
				positive_vectors[i][2] = 1
			elif word.lower() == "dull":
				positive_vectors[i][3] = 1
			elif word.lower() == "effective":
				positive_vectors[i][4] = 1
			elif word.lower() == "enjoyable":
				positive_vectors[i][5] = 1
			elif word.lower() == "great":
				positive_vectors[i][6] = 1
			elif word.lower() == "hilarious":
				positive_vectors[i][7] = 1
	i+=1

i=0
for neg_reviews_file in os.listdir(path_neg):	
	neg_review = open(path_neg+neg_reviews_file, "r")
	vector = [0,0,0,0,0,0,0,0]
	for line in neg_review:
		for word in line.split():
			if word.lower() == "awful":
				vector[0] = 1
			elif word.lower() == "bad":
				vector[1] = 1
			elif word.lower() == "boring":
				vector[2] = 1
			elif word.lower() == "dull":
				vector[3] = 1
			elif word.lower() == "effective":
				vector[4] = 1
			elif word.lower() == "enjoyable":
				vector[5] = 1
			elif word.lower() == "great":
				vector[6] = 1
			elif word.lower() == "hilarious":
				vector[7] = 1
	negative_vectors.append(vector)

positive = np.asarray(positive_vectors)
negative = np.asarray(negative_vectors)


probs_pos = (positive.sum(axis=0).astype(float)+1.0)/1000
probs_neg = (negative.sum(axis=0).astype(float)+1.0)/1000
print(probs_pos)
print(words)

print(probs_neg)
print(words)


