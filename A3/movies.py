#10 Fold version
import numpy as np
from sklearn.datasets import *
from sklearn.naive_bayes import *
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import accuracy_score
import os
import re


#Looad all the review files, according to folder categories
reviews = load_files("/Users/rafa/Downloads/review_polarity/txt_sentoken/")
#Print the categories to check
print("Categories are " + str(reviews.target_names))

#Split the data into train and test
#The test size is set to default sklearn of 25
X_train, X_test, y_train, y_test = train_test_split(
	reviews.data,reviews.target,test_size=0.25,random_state=0)




#Generate the Two Pipelines for each of Multinomial and Bernoulli NB

text_multi = Pipeline([('vect',CountVectorizer()),
					 ('tfidf', TfidfTransformer()),
					 ('clf', MultinomialNB()),
					])

text_bernoulli = Pipeline([('vect',CountVectorizer()),
					 ('tfidf', TfidfTransformer()),
					 ('clf', BernoulliNB()),
					])

#Get the score of the the current train and test
#using Multinomial NB
text_multi.fit(X_train, y_train)
score_multi = text_multi.score(X_test,y_test)
print("The accuracy with split of .25 in test using Multinomial NB is " + str(score_multi*100))

#Get the score of the the current train and test
#using Bernoulli NB
text_bernoulli.fit(X_train, y_train)
score_bernoulli = text_bernoulli.score(X_test,y_test)
print("The accuracy with split of .25 in test using Bernoulli NB is " + str(score_bernoulli*100))


#Get the score of with cross validation with 10 folds to compare
#Using Multinomial Naive Bayes
predicted_multi = cross_val_predict(text_multi,reviews.data,reviews.target,cv=10)
print("The accuracy with 10 fold cross validation with Multinomial NB is " +  str(accuracy_score(reviews.target,predicted_multi)*100))


#Get the score of with cross validation with 10 folds to compare
#Using Bernoulli Naive Bayes
predicted_bernoulli = cross_val_predict(text_bernoulli,reviews.data,reviews.target,cv=10)
print("The accuracy with 10 fold cross validation with Bernoulli NB is " + str(accuracy_score(reviews.target,predicted_bernoulli)*100))