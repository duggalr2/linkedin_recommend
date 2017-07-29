import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from regex import tokenize_and_stem


job_title = pd.read_table('edu_classified', header=None, sep=', ', names=['title', 'label'])
# job_title['label_num'] = job_title.label({'software':0, 'engineering':1, 'research':2, 'design':3, 'data_science':4,
#                                           'product_manager':5, 'business_finance':6, 'startup_founder':7,
#                                           'admin_it':8, 'crypto':9})

# print(job_title)

X = job_title.title
y = job_title.label


X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=2)
vect = CountVectorizer()
X_train_dtm = vect.fit_transform(X_train)  # creates vocab set and dtm for each raw document!
# print(len(vect.get_feature_names()))  # 304
X_test_dtm = vect.transform(X_test)

nb = MultinomialNB()
nb.fit(X_train_dtm, y_train)
y_pred_class = nb.predict(X_test_dtm)  # make class predictions for X_test_dtm
w = list(X_test)

# for i in range(len(y_pred_class)):  # TODO: Look for 'trouble' words;
#     print(w[i], y_pred_class[i])

# print(metrics.accuracy_score(y_test, y_pred_class))

X_train_tokens = vect.get_feature_names()
software_token_count = nb.feature_count_[0, :]  # number of times each token appears across all software titles
engineer_token_count = nb.feature_count_[1, :]
product_token_count = nb.feature_count_[2, :]
business_token_count = nb.feature_count_[3, :]
startup_token_count = nb.feature_count_[4, :]
tokens = pd.DataFrame({'token': X_train_tokens, 'one': software_token_count, 'two': engineer_token_count,
                       'five': product_token_count, 'six': business_token_count, 'seven': startup_token_count})
tokens['one'] = tokens.one + 1
tokens['two'] = tokens.two + 1
tokens['five'] = tokens.five + 1
tokens['six'] = tokens.six + 1
tokens['seven'] = tokens.seven + 1
# nb.class_count_[0]  # counts how many times 0 appears.
tokens['one'] = tokens.one / nb.class_count_[0]
tokens['two'] = tokens.two / nb.class_count_[1]
tokens['five'] = tokens.five / nb.class_count_[2]
tokens['six'] = tokens.size / nb.class_count_[3]
tokens['seven'] = tokens.size / nb.class_count_[4]
# print(tokens.sort_values('one', ascending=False).head(10))  # cs
# print(tokens.sort_values('two', ascending=False).head(10))  # finance
# print(tokens.sort_values('five', ascending=False).head(10))  # engineering
# print(tokens.sort_values('six', ascending=False).head(10))  # engineering
# print(tokens.sort_values('seven', ascending=False).head(10))  # engineering


def predict_program(job_list):
    """Assign a classification to a url"""
    if job_list[0] is not None:
        edu_list = [tokenize_and_stem(i) for i in job_list]
        edu_list = [' '.join(job) for job in edu_list]
        vect = CountVectorizer()
        x_series = pd.Series(X)
        X_train_dtm = vect.fit_transform(x_series)
        y_train = pd.Series(y)
        job_list_series = pd.Series(edu_list)
        job_list_dtm = vect.transform(job_list_series)
        nb = MultinomialNB()
        nb.fit(X_train_dtm, y_train)
        y_pred = nb.predict(job_list_dtm)
        # for i in range(len(job_list)):
        #     print(job_list[i], y_pred[i])
        return y_pred
    else:
        return None


# print(predict_program(('Computer Science and Engineering',)))
