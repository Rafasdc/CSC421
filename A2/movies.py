import numpy as np
import os

path_pos = "/Users/rafa/Downloads/review_polarity/txt_sentoken/pos/"
path_neg = "/Users/rafa/Downloads/review_polarity/txt_sentoken/neg/"
positive_reviews = []
negative_reviews = []
positive_vectors=[]
negative_vectors=[]
words = ["awful","bad","boring","dull","effective","enjoyable","great","hilarious"]

i=0
for pos_reviews_file in os.listdir(path_pos):
	#Append Path
	positive_reviews.append(path_pos+pos_reviews_file)
	#Read the file
	pos_review = open(path_pos+pos_reviews_file, "r")
	#Create initial Vector
	vector = [0,0,0,0,0,0,0,0]
	#Append empty Vector
	positive_vectors.append(vector)
	#Read file line by line
	#And change corresponing position according to words
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

for neg_reviews_file in os.listdir(path_neg):	
	negative_reviews.append(path_neg+neg_reviews_file)
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

#Turn into Numpy Arrays for easier processing
positive = np.asarray(positive_vectors)
negative = np.asarray(negative_vectors)

#Get the Probabilities of each word
probs_pos = (positive.sum(axis=0).astype(float)+1.0)/1000
probs_neg = (negative.sum(axis=0).astype(float)+1.0)/1000

#Print them
print(probs_pos)
print(words)

print(probs_neg)
print(words)

def likelihood(review, probs_for_type):
	probability_product = 1.0
	for (i,w) in enumerate(review):
		#If word in vector
		if (w==1):
			probability=probs_for_type[i]
		else:
			probability= 1.0 - probs_for_type[i]
		probability_product *= probability
	return probability_product


def predict(review):
	scores = [likelihood(review,probs_pos), likelihood(review,probs_neg)]
	labels = ['positive', 'negative']
	return labels[np.argmax(scores)]

def predict_set(test_set, truth_label):
	score = 0
	for r in test_set:
		if predict(r) == truth_label:
			score+=1
	return score/10.0

print(predict_set(positive,'positive'))
print(predict_set(negative,'negative'))
