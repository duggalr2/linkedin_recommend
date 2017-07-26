import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics

url = 'https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/yelp.csv'
yelp = pd.read_csv(url, header=None, names=['business_id','date','review_id','stars','text','type',
                                            'user_id','cool','useful','funny'])
filter_df = yelp[(yelp.stars == '5') | (yelp.stars == '1')] # only movies with 1 and 5 star ratings
X = filter_df.text
y = filter_df.stars
# X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
vect = CountVectorizer()
X_train_dtm = vect.fit_transform(X_train)  # creates vocab set and dtm for each raw document!
X_test_dtm = vect.transform(X_test)

nb = MultinomialNB()
nb.fit(X_train_dtm, y_train)
y_pred_class = nb.predict(X_test_dtm)  # make class predictions for X_test_dtm

# print(metrics.accuracy_score(y_test, y_pred_class))  # 0.918
# print(y_test.value_counts())  # examine the class distribution of the testing set (using a Pandas Series method)
# print(y_test.value_counts().head(1) / len(y_test))  # 0.819961 accuracy could be achieved by predicting most freq class

# print(metrics.confusion_matrix(y_test, y_pred_class))
# print(X_test[y_test < y_pred_class].head(10))  # first 10 false positives (1-star reviews incorrectly classified as 5-star reviews)
# print(X_test[1782])  # example of false positive: words like good impressive nice appear which is why its 5-star...
# print(X_test[y_test > y_pred_class].head(10))  # first 10 false negatives (5-star reviews incorrectly classified as 1-star reviews)

X_train_tokens = vect.get_feature_names()  # Vocab Set
one_token_count = nb.feature_count_[0, :]  # number of times each token appears across all HAM messages
five_token_count = nb.feature_count_[1, :]  # number of times each token appears across all SPAM messages

# create a DataFrame of tokens with their separate ham and spam counts
tokens = pd.DataFrame({'token': X_train_tokens, 'one': one_token_count, 'five': five_token_count})

tokens['one'] = tokens.one + 1
tokens['five'] = tokens.five + 1

tokens['one'] = tokens.one / nb.class_count_[0]
tokens['five'] = tokens.five / nb.class_count_[1]
# print(tokens.sample(5, random_state=6))  # Naive Bayes counts the number of observations in each class

tokens['five_star_ratio'] = tokens.five / tokens.one
tokens['one_star_ratio'] = tokens.one / tokens.five
# print(tokens.sort_values('five_star_ratio', ascending=False).head(10))  # top 10 tokens predictive for 5-star
# print(tokens.sort_values('one_star_ratio', ascending=False).head(10))  # top 10 tokens predictive for 1-star


