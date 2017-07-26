from sklearn.datasets import load_iris
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import CountVectorizer


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


### Part 3:

sms = pd.read_table('sms', header=None, names=['label', 'message'])
print(sms)

