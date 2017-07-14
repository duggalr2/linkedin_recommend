from __future__ import print_function
import sqlite3
import nltk
from nltk.stem.snowball import SnowballStemmer
import operator
import re
import matplotlib.pyplot as plt
import kNN
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer


def get_education():
    conn = sqlite3.connect('/Users/Rahul/Desktop/Main/Side_projects/linkedin_recommend/db.sqlite3')
    c = conn.cursor()
    c.execute('SELECT school_program FROM link_rec_allparsedprofile')
    y = c.fetchall()
    return [i[0] for i in y if i[0] is not None]

education_list = get_education()
for i in education_list:
    print(i)


def filterPick(list, filter, classification):
    """Used for applying the regex search"""
    y = []
    for job in list:
        x = [(job, classification) for l in job for m in (filter(l),) if m]
        y.append(x)
    return y


def cs():
    new_title_list = [tokenize_and_stem(i) for i in education_list]
    searchRegex = re.compile('(computer|software)').search
    x = filterPick(new_title_list, searchRegex, 'computer_science')
    return x


def finance():
    new_title_list = [tokenize_and_stem(i) for i in education_list]
    searchRegex = re.compile('(finance|commerce|business)').search
    x = filterPick(new_title_list, searchRegex, 'computer_science')
    return x








# stopwords = nltk.corpus.stopwords.words('english')  # load the stop words from nltk
# stemmer = SnowballStemmer("english")  # stemming
#
#
# def tokenize_and_stem(text):
#     # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
#     tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
#     filtered_tokens = []
#     # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
#     for token in tokens:
#         if re.search('[a-zA-Z]', token):
#             filtered_tokens.append(token)
#     stems = [stemmer.stem(t) for t in filtered_tokens]
#     return stems
#
#
# def stem_for_regex(items):
#     x = []
#     for i in items:
#         x.append(tokenize_and_stem(i))
#     return [y for i in x for y in i]

