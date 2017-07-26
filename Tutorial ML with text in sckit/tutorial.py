from sklearn.datasets import load_iris
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.linear_model import LogisticRegression


### Part 1:


# load the iris dataset
iris = load_iris()
# store the feature matrix (X) and response vector (y)
X = iris.data
y = iris.target

# for i in range(len(X)):
#     print(X[i], y[i])

# print(X.shape)
# print(y.shape)

# print(pd.DataFrame(X, columns=iris.feature_names).head())

# instantiate the model (with the default parameters)
knn = KNeighborsClassifier()

# fit the model with data (occurs in-place)
knn.fit(X, y)

# print(knn.predict([[3, 5, 4, 2]]))


### Part 2:

# example text for model training (SMS messages)
simple_train = ['call you tonight', 'Call me a cab', 'please call me... PLEASE!']

vect = CountVectorizer()  # import and instantiate CountVectorizer (with the default parameters)
vect.fit(simple_train)  # learn the 'vocabulary' of the training data (occurs in-place)
# print(vect.get_feature_names())  # examine the fitted vocabulary; It's the VocabSet!

simple_train_dtm = vect.transform(simple_train)  # transform training data into a 'document-term matrix'
# Document-term matrix: describes the frequency of terms that occur in collection of documents

# print(simple_train_dtm)  # type: <class 'scipy.sparse.csr.csr_matrix'>

# simple_train_dtm.toarray()  # convert sparse matrix to a dense matrix (same matrix as my implementation)

# examine the vocabulary and document-term matrix together! <-- this makes it so much easier to read!
pd.DataFrame(simple_train_dtm.toarray(), columns=vect.get_feature_names())

simple_test = ["please don't call me"]
simple_test_dtm = vect.transform(simple_test)
# simple_test_dtm.toarray()
# print(pd.DataFrame(simple_test_dtm.toarray(), columns=vect.get_feature_names()))

# # Steps for ML Model: import, instantiate, fit, predict
# # Steps for CountVectorizer: import, instantiate, fit, transform (doesn't predict just transforms data)


### Part 3: Naive Bayes

sms = pd.read_table('sms', header=None, names=['label', 'message'])
#
# # print(sms.shape)  # examine the shape
# # print(sms.head(10))  # examine the first 10 rows
# # print(sms.label.value_counts())  # Class Distribution!!!!!!!!
#
sms['label_num'] = sms.label.map({'ham':0, 'spam':1})  # convert class to 0 and 1's!! SO MUCH EASIER
X = sms.message
y = sms.label_num
# # print(X.shape)
# # print(y.shape)

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)  # automatically converts to train/test
# # print(X_train.shape)
# # print(X_test.shape)
# # print(y_train.shape)
# # print(y_test.shape)

vect = CountVectorizer()
X_train_dtm = vect.fit_transform(X_train)  # equivalently: combine fit and transform into a single step
X_test_dtm = vect.transform(X_test)  # transform testing data (using fitted vocabulary) into a document-term matrix

nb = MultinomialNB()
nb.fit(X_train_dtm, y_train)
# y_pred_class = nb.predict(X_test_dtm)  # make class predictions for X_test_dtm
# # print(metrics.accuracy_score(y_test, y_pred_class))
# # print(metrics.confusion_matrix(y_test, y_pred_class))
# y_pred_prob = nb.predict_proba(X_test_dtm)[:, 1]  # calculate predicted probabilities for X_test_dtm
# # print(y_pred_prob)
# # print(metrics.roc_auc_score(y_test, y_pred_prob))  # AUC: area under the curve


### Part 4: Logisitic Regression

logreg = LogisticRegression()
logreg.fit(X_train_dtm, y_train)
y_pred_class = logreg.predict(X_test_dtm)
y_pred_prob = logreg.predict_proba(X_test_dtm)[:, 1]
# print(metrics.accuracy_score(y_test, y_pred_class))
# print(metrics.confusion_matrix(y_test, y_pred_class))
# print(metrics.roc_auc_score(y_test, y_pred_prob))

### Part 5: Calculating spamminess of each token

X_train_tokens = vect.get_feature_names()  # store the vocabulary of X_train
# print(len(X_train_tokens))
# print(X_train_tokens[0:50])
# print(X_train_tokens[-50:])
# print(nb.feature_count_)  # Naive Bayes counts the number of times each token appears in each class

ham_token_count = nb.feature_count_[0, :]  # number of times each token appears across all HAM messages
spam_token_count = nb.feature_count_[1, :]  # number of times each token appears across all SPAM messages

# create a DataFrame of tokens with their separate ham and spam counts
tokens = pd.DataFrame({'token':X_train_tokens, 'ham':ham_token_count, 'spam':spam_token_count})
# print(tokens)
# print(tokens.head())
# print(tokens.sample(5, random_state=6))  # Naive Bayes counts the number of observations in each class


# add 1 to ham and spam counts to avoid dividing by 0
tokens['ham'] = tokens.ham + 1
tokens['spam'] = tokens.spam + 1
# print(tokens.sample(5, random_state=6))

# convert the ham and spam counts into frequencies
tokens['ham'] = tokens.ham / nb.class_count_[0]
tokens['spam'] = tokens.spam / nb.class_count_[1]
# print(tokens.sample(5, random_state=6))

# calculate the ratio of spam-to-ham for each token
tokens['spam_ratio'] = tokens.spam / tokens.ham
# print(tokens.sample(5, random_state=6))

# print(tokens.sort_values('spam_ratio', ascending=False))  # DataFrame sorted by spam ratio
