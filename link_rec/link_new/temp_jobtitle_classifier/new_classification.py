from __future__ import print_function
import sqlite3
import nltk
from nltk.stem.snowball import SnowballStemmer
import operator
import re
import matplotlib.pyplot as plt
import numpy as np
from sklearn.manifold import TSNE
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer


def get_job_title():
    conn = sqlite3.connect('/Users/Rahul/Desktop/Main/Side_projects/linkedin_recommend/db.sqlite3')
    c = conn.cursor()
    c.execute('SELECT job FROM link_rec_alljobtitle')
    y = c.fetchall()
    job_title = [job[0].lower() for job in y]
    c.execute('SELECT loc FROM link_rec_alllocation')
    y = c.fetchall()
    company_name = [i[0].lower() for i in y]
    c.execute('SELECT url FROM link_rec_allparsedprofile')
    y = c.fetchall()
    profile_url = [i[0] for i in y]
    return job_title, company_name, profile_url


stopwords = nltk.corpus.stopwords.words('english')  # load the stop words from nltk
stemmer = SnowballStemmer("english")  # stemming


def tokenize_and_stem(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems


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


def prepare_ds(raw_training_ds, vocabSet):
    return [bag_of_words(vocabSet, sentence) for sentence in raw_training_ds]


if __name__ == '__main__':
    lines = open(
        '/Users/Rahul/Desktop/Main/Side_projects/linkedin_recommend/link_rec/link_new/temp_jobtitle_classifier/job_classified').readlines()
    lines = [line.replace('\n', '') for line in lines]
    train_list, train_labels = [], []
    big_list = []
    for line in lines:
        other_line = line.split(' ')
        train_list.append(tokenize_and_stem(' '.join(other_line[:-1])))
        line = line.split(', ')
        train_labels.append(line[-1])
        # train_list.append(line[:-1])
        big_list.append((line[:-1], line[-1]))

    vocab_set = vocabSet(train_list)

    vectorized_training = prepare_ds(train_list, vocab_set)
    tsne = TSNE(n_components=2, random_state=0)
    x_test_2d = tsne.fit_transform(vectorized_training)
    markers=('s', 'd', 'o', '^', 'v', 'r', 'w', 'y', 'p', 'c')
    # color_map = {0:'red', 1:'blue', 2:'lightgreen', 3:'purple', 4:'cyan'}
    plt.figure()
    for idx, cl in enumerate(np.unique(train_labels)):
        print(idx, cl)
        plt.scatter(x=x_test_2d[train_labels==idx], y=x_test_2d[train_labels==idx], marker=markers[idx], label=cl)
    # plt.xlabel('X in t-SNE')
    # plt.ylabel('Y in t-SNE')
    # plt.legend(loc='upper left')
    # plt.title('t-SNE visualization of test data')
    # plt.show()












# test_job_title, company_name, profile_url = get_job_title()
# test_job_title = [tokenize_and_stem(i) for i in test_job_title]
# new_test_job_title = []
# for y in test_job_title:
#     st = ' '.join(y)
#     new_test_job_title.append(st)


# def searchBS(big_list):
#     start_index = 0
#     new_end_index = 1
#     new_big_list = [list(i) for i in big_list]
#
#     while start_index < new_end_index:
#
#         new_end_index = len(new_big_list)
#         duplicate = []
#
#         for index in range(start_index, new_end_index):
#             item = new_big_list[index]
#             if item[0] == new_big_list[start_index][0] and item[-1] != new_big_list[start_index][
#                 -1] and index != start_index:
#                 new_big_list[start_index].append(item[-1])
#                 duplicate.append(new_big_list[index])
#
#         for item in duplicate:
#             i = new_big_list.index(item)
#             del new_big_list[i]
#
#         start_index += 1
#     return new_big_list


# li = searchBS(big_list)





# Multi-label kNN Classification

# new_class = []
# new_job_title = []
#
# for i in li:
#     new_class.append(i[1:])
#     new_job_title.append(i[0])
#
#
# new_job_title_list = []
# for y in new_job_title:
#     st = ''.join(y)
#     new_job_title_list.append(st)
#
# X_train = np.array(new_job_title_list)
# y_train_text = new_class
#
# mlb = MultiLabelBinarizer()
# Y = mlb.fit_transform(y_train_text)
#
# classifier = Pipeline([
#     ('vectorizer', CountVectorizer()),
#     ('tfidf', TfidfTransformer()),
#     ('clf', OneVsRestClassifier(LinearSVC()))
# ])


# classifier.fit(X_train, Y)
#
# test_data = np.array(new_test_job_title)
# predicted = classifier.predict(test_data)
# all_labels = mlb.inverse_transform(predicted)
# for item, labels in zip(X_train, all_labels):
#     print('{0} => {1}'.format(item, ', '.join(labels)))

# with open('new_classification_job', 'a') as f:
#     for item, labels in zip(X_train, all_labels):
#         f.write('{0} => {1}'.format(item, ', '.join(labels)))
#         f.write('\n')
