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


def stem_for_regex(items):
    x = []
    for i in items:
        x.append(tokenize_and_stem(i))
    return [y for i in x for y in i]


def filterPick(list, filter, classification):
    """Used for applying the regex search"""
    y = []
    for job in list:
        x = [(job, classification) for l in job for m in (filter(l),) if m]
        y.append(x)
    return y


def cs():
    new_title_list = [tokenize_and_stem(i) for i in education_list]
    searchRegex = re.compile('(comput|softwar|secur)').search
    x = filterPick(new_title_list, searchRegex, 'computer_science')
    return x


def finance():
    new_title_list = [tokenize_and_stem(i) for i in education_list]
    searchRegex = re.compile('(financ|commerc|busi|manag|account|market)').search
    x = filterPick(new_title_list, searchRegex, 'business')
    return x


def engineer():
    new_title_list = [tokenize_and_stem(i) for i in education_list]
    searchRegex = re.compile('(mechan|engi|aerospac|electr|robot|bioengin|civil|mechatron|chemic)').search
    x = filterPick(new_title_list, searchRegex, 'engineering')
    return x


def math_sciences():
    new_title_list = [tokenize_and_stem(i) for i in education_list]
    searchRegex = re.compile('(mathemat|math|physic|statist)').search
    x = filterPick(new_title_list, searchRegex, 'math/physics/statistics')
    return x


def humanties_lifesci():
    new_title_list = [tokenize_and_stem(i) for i in education_list]
    searchRegex = re.compile('(polit|biolog|psycholog|neurosci|nurs)').search
    x = filterPick(new_title_list, searchRegex, 'humanities/lifesci')
    return x


def write_to_file(items):
    for i in items:
        if len(i) != 0:
            with open('edu_classified', 'a') as f:
                job = ' '.join(i[0][0])
                classification = i[0][1]
                f.write(job + ', ' + classification + '\n')

# write_to_file(cs())
# write_to_file(finance())
# write_to_file(engineer())
# write_to_file(math_sciences())
# write_to_file(humanties_lifesci())


def count(data):
    """
    Return's a dict with key (item) and number of times it appears in list
    """
    assert type(data) == list
    main_di = {}
    for i in data:
        if i in main_di:
            main_di[i] += 1
        else:
            main_di[i] = 1
    return main_di


lines = open('edu_classified').readlines()
lines = [line.replace('\n', '') for line in lines]
classification = []
for i in lines:
    c = i.split(',')[-1]
    classification.append(c)


def barGraph(data_count):

    names, count_in = [], []
    data_count = sorted(data_count.items(), key=operator.itemgetter(1), reverse=True)
    for i in data_count:
        names.append(i[0])
        count_in.append(i[-1])

    plt.rcdefaults()
    fig, ax = plt.subplots()
    y_pos = np.arange(len(names))
    ax.barh(y_pos, count_in, align='center',
            color='green', ecolor='black')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(names)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Categories')
    ax.set_title('# of job titles in each category')
    plt.show()

data_count = count(classification)
barGraph(data_count)


lines = open('edu_classified').readlines()
lines = [line.replace('\n', '') for line in lines]
job_list, job_class, big_list = [], [], []
for line in lines:
    new_line = line.split(', ')
    job_class.append(new_line[-1])
    job_list.append(new_line[:-1])
    big_list.append((new_line[:-1], new_line[-1]))


def searchBS(big_list):
    start_index = 0
    # end_index = len(big_list)
    new_end_index = 1
    new_big_list = [list(i) for i in big_list]

    while start_index < new_end_index:

        new_end_index = len(new_big_list)
        duplicate = []

        for index in range(start_index, new_end_index):
            item = new_big_list[index]
            if item[0] == new_big_list[start_index][0] and item[-1] != new_big_list[start_index][
                -1] and index != start_index:
                new_big_list[start_index].append(item[-1])
                duplicate.append(new_big_list[index])

        for item in duplicate:
            i = new_big_list.index(item)
            del new_big_list[i]

        start_index += 1
    return new_big_list

li = searchBS(big_list)
new_class = []
new_job_title = []

for i in li:
    new_class.append(i[1:])
    new_job_title.append(i[0])


new_job_title_list = []
for y in new_job_title:
    st = ''.join(y)
    new_job_title_list.append(st)

X_train = np.array(new_job_title_list)
y_train_text = new_class

mlb = MultiLabelBinarizer()
Y = mlb.fit_transform(y_train_text)

classifier = Pipeline([
    ('vectorizer', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', OneVsRestClassifier(LinearSVC()))])

classifier.fit(X_train, Y)
predicted = classifier.predict(X_train)
all_labels = mlb.inverse_transform(predicted)

for item, labels in zip(X_train, all_labels):
    print('{0} => {1}'.format(item, ', '.join(labels)))
