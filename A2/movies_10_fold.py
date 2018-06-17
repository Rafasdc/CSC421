#10 Fold version
import numpy as np
import os
import re

path_pos = "/Users/rafa/Downloads/review_polarity/txt_sentoken/pos/"
path_neg = "/Users/rafa/Downloads/review_polarity/txt_sentoken/neg/"
all_reviews = []
positive_reviews = []
negative_reviews = []
positive_vectors=[]
negative_vectors=[]
folds_pos = [[],[],[],[],[],[],[],[],[],[]]
folds_neg = [[],[],[],[],[],[],[],[],[],[]]
words = ["awful","bad","boring","dull","effective","enjoyable","great","hilarious"]


for pos_reviews_file in os.listdir(path_pos):
	m = re.search('(?<=cv)(.*)(?=_)',pos_reviews_file)
	num = int(m.group())

	all_reviews.append(path_pos+pos_reviews_file)
	positive_reviews.append(path_pos+pos_reviews_file)
	pos_review = open(path_pos+pos_reviews_file, "r")
	vector = [0,0,0,0,0,0,0,0]

	fold = 0
	if num <= 99:
		folds_pos[0].append(vector)
		fold = 0
	elif num >99 and num <= 199:
		folds_pos[1].append(vector)
		fold = 1
	elif num > 199 and num <= 299:
		folds_pos[2].append(vector)
		fold = 2
	elif num > 299 and num <= 399:
		folds_pos[3].append(vector)
		fold = 3
	elif num > 399 and num <= 499:
		folds_pos[4].append(vector)
		fold = 4
	elif num > 499 and num <= 599:
		folds_pos[5].append(vector)
		fold = 5
	elif num > 599 and num <= 699:
		folds_pos[6].append(vector)
		fold = 6
	elif num > 699 and num <= 799:
		folds_pos[7].append(vector)
		fold = 7
	elif num > 799 and num <= 899:
		folds_pos[8].append(vector)
		fold = 8
	elif num > 899 and num <= 999:
		folds_pos[9].append(vector)
		fold = 9

	for line in pos_review:
		for word in line.split():
			if word.lower() == "awful":
				folds_pos[fold][len(folds_pos[fold])-1][0] = 1
			elif word.lower() == "bad":
				folds_pos[fold][len(folds_pos[fold])-1][1] = 1
			elif word.lower() == "boring":
				folds_pos[fold][len(folds_pos[fold])-1][2] = 1
			elif word.lower() == "dull":
				folds_pos[fold][len(folds_pos[fold])-1][3] = 1
			elif word.lower() == "effective":
				folds_pos[fold][len(folds_pos[fold])-1][4] = 1
			elif word.lower() == "enjoyable":
				folds_pos[fold][len(folds_pos[fold])-1][5] = 1
			elif word.lower() == "great":
				folds_pos[fold][len(folds_pos[fold])-1][6] = 1
			elif word.lower() == "hilarious":
				folds_pos[fold][len(folds_pos[fold])-1][7] = 1


for neg_reviews_file in os.listdir(path_neg):
	m = re.search('(?<=cv)(.*)(?=_)',neg_reviews_file)
	num = int(m.group())
	all_reviews.append(path_neg+neg_reviews_file)
	negative_reviews.append(path_neg+neg_reviews_file)
	neg_review = open(path_neg+neg_reviews_file, "r")

	vector = [0,0,0,0,0,0,0,0]

	fold = 0
	if num <= 99:
		folds_neg[0].append(vector)
		fold = 0
	elif num >99 and num <= 199:
		folds_neg[1].append(vector)
		fold = 1
	elif num > 199 and num <= 299:
		folds_neg[2].append(vector)
		fold = 2
	elif num > 299 and num <= 399:
		folds_neg[3].append(vector)
		fold = 3
	elif num > 399 and num <= 499:
		folds_neg[4].append(vector)
		fold = 4
	elif num > 499 and num <= 599:
		folds_neg[5].append(vector)
		fold = 5
	elif num > 599 and num <= 699:
		folds_neg[6].append(vector)
		fold = 6
	elif num > 699 and num <= 799:
		folds_neg[7].append(vector)
		fold = 7
	elif num > 799 and num <= 899:
		folds_neg[8].append(vector)
		fold = 8
	elif num > 899 and num <= 999:
		folds_neg[9].append(vector)
		fold = 9

	for line in neg_review:
		for word in line.split():
			if word.lower() == "awful":
				folds_neg[fold][len(folds_neg[fold])-1][0] = 1
			elif word.lower() == "bad":
				folds_neg[fold][len(folds_neg[fold])-1][1] = 1
			elif word.lower() == "boring":
				folds_neg[fold][len(folds_neg[fold])-1][2] = 1
			elif word.lower() == "dull":
				folds_neg[fold][len(folds_neg[fold])-1][3] = 1
			elif word.lower() == "effective":
				folds_neg[fold][len(folds_neg[fold])-1][4] = 1
			elif word.lower() == "enjoyable":
				folds_neg[fold][len(folds_neg[fold])-1][5] = 1
			elif word.lower() == "great":
				folds_neg[fold][len(folds_neg[fold])-1][6] = 1
			elif word.lower() == "hilarious":
				folds_neg[fold][len(folds_neg[fold])-1][7] = 1


fold_pos = np.asarray(folds_pos)
fold_neg = np.asarray(folds_neg)

probs_pos = (fold_pos.sum(axis=1).astype(float)+1.0)/100
probs_neg = (fold_neg.sum(axis=1).astype(float)+1.0)/100
print(probs_pos)
print(probs_neg)


def likelihood(review, probs_for_type,fold):
	probability_product = 1.0
	for (i,w) in enumerate(review):
		if (w==1):
			probability=probs_for_type[fold][i]
		else:
			probability= 1.0 - probs_for_type[fold][i]
		probability_product *= probability
	return probability_product


def predict(review,fold):
	scores = [likelihood(review,probs_pos,fold), likelihood(review,probs_neg,fold)]
	labels = ['positive', 'negative']
	return labels[np.argmax(scores)]

def predict_set(test_set, truth_label,fold):
	score = 0
	for r in test_set:
		if predict(r,fold) == truth_label:
			score+=1
	return score


averages_positive = []
averages_negative = []

for i in range(10):
	pos_score = predict_set(folds_pos[i],'positive',i)
	averages_positive.append(pos_score)
	print(pos_score)

for j in range(10):
	neg_score = predict_set(folds_neg[i],'negative',i)
	averages_negative.append(neg_score)
	print(neg_score)


print(np.mean(averages_positive))
print(np.mean(averages_negative))

'''
print(predict(positive[98]))
print(predict(negative[83]))

print(predict_set(positive,'positive'))
print(predict_set(negative,'negative'))
'''
