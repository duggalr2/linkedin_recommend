import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from link_rec.link_new.temp_jobtitle_classifier import regex
import sqlite3

path = '/Users/Rahul/Desktop/Main/Side_projects/linkedin_recommend/link_rec/link_new/temp_jobtitle_classifier/job_classified'
job_title = pd.read_table(path, header=None, sep='=>', names=['title', 'label'])
# job_title['label_num'] = job_title.label({'software':0, 'engineering':1, 'research':2, 'design':3, 'data_science':4,
#                                           'product_manager':5, 'business_finance':6, 'startup_founder':7,
#                                           'admin_it':8, 'crypto':9})

X = job_title.title
y = job_title.label

# print(y.value_counts().sort_index())  # make sure all 10 labels are there


def train_test():
    """Identify accuracy via training set"""
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=2)
    vect = CountVectorizer()
    X_train_dtm = vect.fit_transform(X_train)  # creates vocab set and dtm for each raw document!
    X_test_dtm = vect.transform(X_test)

    nb = MultinomialNB()
    nb.fit(X_train_dtm, y_train)
    y_pred_class = nb.predict(X_test_dtm)  # make class predictions for X_test_dtm
    # w = list(X_test)
    return metrics.accuracy_score(y_test, y_pred_class)


def predict_job(job_list):
    """Assign a classification to a url"""
    # TODO: Add case where len is 1 or 0....
    job_list = [job for j in job_list for job in j]
    new_job_list = [regex.tokenize_and_stem(i) for i in job_list]
    new_job_list = [' '.join(job) for job in new_job_list]
    vect = CountVectorizer()
    x_series = pd.Series(X)
    X_train_dtm = vect.fit_transform(x_series)
    y_train = pd.Series(y)
    job_list_series = pd.Series(new_job_list)
    job_list_dtm = vect.transform(job_list_series)
    nb = MultinomialNB()
    nb.fit(X_train_dtm, y_train)
    y_pred = nb.predict(job_list_dtm)
    # for i in range(len(job_list)):
    #     print(job_list[i], y_pred[i])
    return y_pred

# print(predict_job([('Founder',), ('Founder',), ('Architect & Full-stack developer',), ('Senior Engineer',), ('Technical Consultant',)]))


def get_profile_info(profile_id):
    conn = sqlite3.connect('/Users/Rahul/Desktop/Main/Side_projects/linkedin_recommend/db.sqlite3')
    c = conn.cursor()
    sql = 'SELECT id, name, header, url, school, school_program FROM link_rec_allparsedprofile WHERE id=?'
    c.execute(sql, (profile_id,))
    profile_info = c.fetchone()
    sql = 'SELECT job FROM link_rec_alljobtitle WHERE profile_id=?'
    c.execute(sql, (profile_id,))
    job_list = c.fetchall()
    sql = 'SELECT loc FROM link_rec_alllocation WHERE profile_id=?'
    c.execute(sql, (profile_id,))
    job_loc_list = c.fetchall()
    major_dict = {}
    major_dict['profile_info'] = list(profile_info)
    major_dict['job_list'] = job_list
    major_dict['job_loc_list'] = job_loc_list
    return major_dict

print(get_profile_info(112))


def recommend_industry(industry_interest):
    industry_map = {'software': 0, 'engineering': 1, 'research': 2, 'design': 3, 'data_science': 4,
                                                   'product_manager':5, 'business_finance':6, 'startup_founder':7,
                                                   'admin_it':8, 'crypto':9}
    for i in industry_interest:
        if i in industry_map.keys():
            industry_interest[industry_interest.index(i)] = industry_map.get(i)

    conn = sqlite3.connect('/Users/Rahul/Desktop/Main/Side_projects/linkedin_recommend/db.sqlite3')
    c = conn.cursor()
    major_list = []
    for interest in industry_interest:
        sql = 'SELECT profile_id FROM link_rec_alljobtitle WHERE job_classification=?'
        c.execute(sql, (interest,))
        y = c.fetchall()
        y = [i[0] for i in y]
        major_list.append(y)
    major_list = [y for i in major_list for y in i]
    return list(set(major_list))


# if __name__ == '__main__':
#     print(train_test())






# print(y_test.value_counts().head(1) / y_test.shape)
# print(metrics.confusion_matrix(y_test, y_pred_class))
# print(X_test[(y_test == 0) & (y_pred_class != 0)].head(10))
# print(X_test[(y_test == 1) & ((y_pred_class != 1))].head(10))
# print(X_test[(y_test == 5) & ((y_pred_class != 5))].head(10))
# print(X_test[(y_test == 6) & ((y_pred_class != 6))].head(10))
# print(X_test[(y_test == 7) & ((y_pred_class != 7))].head(10))

# for i in range(len(y_pred_class)):  # TODO: Look for 'trouble' words;
#     print(w[i], y_pred_class[i])


# X_train_tokens = vect.get_feature_names()
# software_token_count = nb.feature_count_[0, :]  # number of times each token appears across all software titles
# engineer_token_count = nb.feature_count_[1, :]
# product_token_count = nb.feature_count_[5, :]
# business_token_count = nb.feature_count_[6, :]
# startup_token_count = nb.feature_count_[7, :]
# tokens = pd.DataFrame({'token': X_train_tokens, 'one': software_token_count, 'two': engineer_token_count,
#                        'five': product_token_count, 'six': business_token_count, 'seven': startup_token_count})
# tokens['one'] = tokens.one + 1
# tokens['two'] = tokens.two + 1
# tokens['five'] = tokens.five + 1
# tokens['six'] = tokens.six + 1
# tokens['seven'] = tokens.seven + 1
# # nb.class_count_[0]  # counts how many times 0 appears.
# tokens['one'] = tokens.one / nb.class_count_[0]
# tokens['two'] = tokens.two / nb.class_count_[1]
# tokens['five'] = tokens.five / nb.class_count_[5]
# tokens['six'] = tokens.size / nb.class_count_[6]
# tokens['seven'] = tokens.size / nb.class_count_[7]
# print(tokens.sort_values('one', ascending=False).head(10))  # good
# print(tokens.sort_values('two', ascending=False).head(10))  # good
# print(tokens.sort_values('five', ascending=False).head(10))  # good
# print(tokens.sort_values('six', ascending=False).head(10))
# print(tokens.sort_values('seven', ascending=False).head(10))


