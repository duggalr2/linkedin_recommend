import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics

url = 'https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/yelp.csv'
yelp = pd.read_csv(url, header=None, names=['business_id','date','review_id','stars','text','type',
                                            'user_id','cool','useful','funny'])
X = yelp.text
y = yelp.stars

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
vect = CountVectorizer()
X_train_dtm = vect.fit_transform(X_train)  # creates vocab set and dtm for each raw document!
X_test_dtm = vect.transform(X_test)

nb = MultinomialNB()
nb.fit(X_train_dtm, y_train)
y_pred_class = nb.predict(X_test_dtm)  # make class predictions for X_test_dtm

print(metrics.accuracy_score(y_test, y_pred_class))  # 48%
print(y_test.value_counts().head(1) / y_test.shape)  # calculate the null accuracy:  0.352659
print(metrics.classification_report(y_test, y_pred_class))  # classification report

# Class 1 has low recall, meaning that the model has a hard time detecting the 1-star reviews,
#  but high precision, meaning that when the model predicts a review is 1-star, it's usually correct.
# Class 5 has high recall and precision, probably because 5-star reviews have polarized language,
# and because the model has a lot of observations to learn from.
