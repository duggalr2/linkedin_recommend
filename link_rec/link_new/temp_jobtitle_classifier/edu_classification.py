import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
import numpy as np
from link_rec.link_new.temp_jobtitle_classifier import regex
import sqlite3
from link_rec.link_new.temp_jobtitle_classifier import nb_classification

path = '/Users/Rahul/Desktop/Main/Side_projects/linkedin_recommend/link_rec/link_new/temp_jobtitle_classifier/edu_classified'
job_title = pd.read_table(path, header=None, sep=', ', names=['title', 'label'])
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


def predict_program(job_list, X, y):
    """Assign a classification to a url"""
    if job_list[0] is not None:
        edu_list = [regex.tokenize_and_stem(i) for i in job_list]
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

# conn = sqlite3.connect('/Users/Rahul/Desktop/Main/Side_projects/linkedin_recommend/db.sqlite3')
# c = conn.cursor()
# sql = 'SELECT url FROM link_rec_allparsedprofile WHERE id=?'
# # c.execute(sql, (68,))
# # print(update_profile(c.fetchone()[0]))
# for i in range(0, 228):
#     sql = 'SELECT url FROM link_rec_allparsedprofile WHERE id=?'
#     c.execute(sql, (i,))
#     url = c.fetchone()
#     sql = "SELECT id, school_program FROM link_rec_allparsedprofile WHERE url= ?"
#     c.execute(sql, (url[0],))
#     school_program = c.fetchone()
#     if school_program[-1] is not None:
#         prediction = predict_program(school_program[1:])
#         # print(prediction)
#         sql = 'UPDATE link_rec_allparsedprofile SET program_classification=? WHERE id=?'
#         i = prediction[0]
#         c.execute(sql, (int(i), school_program[0]))
#         conn.commit()



# conn = sqlite3.connect('/Users/Rahul/Desktop/Main/Side_projects/linkedin_recommend/db.sqlite3')
# c = conn.cursor()
# sql = "SELECT id, school_program FROM link_rec_allparsedprofile WHERE url= ?"
# c.execute(sql, ('https://www.linkedin.com/in/karalabe/',))
# school_program = c.fetchone()
# if school_program[-1] is not None:
#     # print(school_program[1:])
#     prediction = predict_program(school_program[1:])
#     # print(prediction)


# print(predict_program(('Computer Science and Engineering',)))


def recommend_program(program_interest):
    edu_map = {'computer_science':0, 'commerce_business':1, 'engineering':2, 'humanities_lifesci':3,
               'math_physics_statistics':4}

    for i in program_interest:
        if i in edu_map.keys():
            program_interest[program_interest.index(i)] = edu_map.get(i)

    conn = sqlite3.connect('/Users/Rahul/Desktop/Main/Side_projects/linkedin_recommend/db.sqlite3')
    c = conn.cursor()
    major_list = []

    for interest in program_interest:
        sql = 'SELECT id FROM link_rec_allparsedprofile WHERE program_classification=?'
        c.execute(sql, (interest,))
        y = c.fetchall()
        y = [i[0] for i in y]
        major_list.append(y)
    major_list = [y for i in major_list for y in i]
    return list(set(major_list))


def find_intersection(one_li, second_li):
    new_int = []
    for i in one_li:
        for k in second_li:
            if i.get('url') == k.get('url'):
                mon = i
                if mon not in new_int:
                    new_int.append(mon)
    return new_int

x = recommend_program(['computer_science', 'commerce_business', 'engineering'])
y = nb_classification.recommend_industry(['software', 'data_science', 'research'])
li = [nb_classification.get_profile_info(i) for i in x]
# for i in li:
#     print(i)
other_li = [nb_classification.get_profile_info(i) for i in y]
# new_int = find_intersection(li, other_li)
# for i in new_int:
#     print(i)


# new_int = []

# for i in other_li:
#     print(i)
    # for k in li:
    #     if i.get('url') == k.get('url'):
    #         mon = i
    #         if mon not in new_int:
    #             new_int.append(mon)


def intersection_school_name(intersection_list):
    conn = sqlite3.connect('/Users/Rahul/Desktop/Main/Side_projects/linkedin_recommend/db.sqlite3')
    c = conn.cursor()
    school_name, id_list = [], []
    for i in intersection_list:
        url = i.get('profile_info')[3]
        sql = 'SELECT id, school FROM link_rec_allparsedprofile WHERE url=?'
        c.execute(sql, (url,))
        y = c.fetchone()
        if y[-1] is not None:
            school_name.append(y[-1])
            id_list.append(y[0])
    return list(zip(id_list, school_name))


def vocabSet(data):
    """
    Create's a Vocab Set: List of unique word's
    Parameter: Parsed Data
    """
    new_set = set([])
    for w in data:
        new_set = new_set | set(w)
    return list(new_set)


def bag_of_words(vocabSet, row):
    """
    Create's a Word Vector using Bag of Word Approach
    Parameter: Vocab Set, Row of Parsed Data;
    """
    returnVec = [0] * len(vocabSet)
    for word in row:
        if word in vocabSet:
            returnVec[vocabSet.index(word)] += 1
    return returnVec


def cosine_similarity(x1, x2):
    """
    Calculate's Cosine Similarity of 2 Word Vector's
    """
    vec1 = np.array(x1)
    vec2 = np.array(x2)
    dot = np.dot(vec1, vec2)
    magnitude1 = np.linalg.norm(vec1)
    magnitude2 = np.linalg.norm(vec2)
    if magnitude1 != 0 and magnitude2 != 0:
        return dot / (magnitude1 * magnitude2)
    return 'With our data, I cannot come up with a rating...'  # TODO: Need to add case where this get's called


def cosine_school(big_list, school_name):
    assert type(school_name) == str
    new_school_name = [(i[0], regex.tokenize_and_stem(i[-1])) for i in big_list]
    school_name_vs = [i[-1] for i in new_school_name]
    vs = vocabSet(school_name_vs)
    dtm_big_list = [(row[0], bag_of_words(vs, row[-1])) for row in new_school_name]
    dtm = regex.tokenize_and_stem(' '.join(school_name.split('_')))
    school_dtm = bag_of_words(vs, dtm)
    cosine_list = [(i[0], cosine_similarity(i[-1], school_dtm)) for i in dtm_big_list]
    sorted_by_second = sorted(cosine_list, key=lambda tup: tup[-1], reverse=True)
    return sorted_by_second

# big_list = intersection_school_name(new_int)
# print(cosine_school(big_list, 'university_of_toronto'))


# cosine_sim_list = cosine_school(intersection_school_name(new_int), 'university_of_toronto')
# cosine_sim_list.sort(reverse=True)  # TODO: room for optimization here..


