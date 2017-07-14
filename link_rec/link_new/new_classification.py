from __future__ import print_function
import sqlite3
import numpy as np
import pandas as pd
import nltk
from nltk.stem.snowball import SnowballStemmer
import matplotlib.pyplot as plt
import operator
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.externals import joblib
import os
import codecs
from sklearn import feature_extraction
import mpld3


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

job_title, company_name, profile_url = get_job_title()

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

import re

# l = ['software', 'developer', 'engineering', 'engineer', 'website', 'web', 'forward', 'deployed',
#      'development', 'fullstack', 'python', 'java', 'agile', 'programmer']
# software_search = []
# for i in l:
#     software_search.append(tokenize_and_stem(i))
# software_search = [y for i in software_search for y in i]

# ['softwar', 'develop', 'engin', 'engin', 'websit', 'web', 'forward', 'deploy', 'develop', 'fullstack', 'python', 'java', 'agil', 'programm']

# for i in job_title:
#     new_title = tokenize_and_stem(i)
#     print([m.group(1) for l in new_title for m in re.search('(softwar|develop|engin|websit|web|forward|deploy|develop|fullstack|python|java|agil|programm)', l) if m])
        # re.search('(softwar|develop|engin|websit|web|forward|deploy|develop|fullstack|python|java|agil|programm)', new_title)


def stem_for_regex(items):
    x = []
    for i in items:
        x.append(tokenize_and_stem(i))
    return [y for i in x for y in i]

# print(stem_for_regex(['fellow']))

# l = ['mechanical', 'industrial', 'skule', 'drilling', 'robotic', 'electrical']
# print(stem_for_regex(l))


# l = ['financial', 'accounts payable', 'records clerk', 'business', 'business development',
#      'business analyst', 'operations', 'logistics', 'marketing', 'business intelligence',
#      'digital marketing',  'investment', 'investment banking', 'capital markets',
#      'venture', 'mergers', 'acquisitions', 'consultant', 'accountant', 'private equity']
# print(stem_for_regex(l))

# l = ['co-founder', 'founder', 'president', 'chief executive officer', 'vice-president']
# print(stem_for_regex(l))



def filterPick(list, filter, classification):
    """Used for applying the regex search"""
    y = []
    empty = []
    for job in list:
        # x = [(job, m.group(1)) for l in job for m in (filter(l),) if m]
        x = [(job, classification) for l in job for m in (filter(l),) if m]
        y.append(x)
        # if len(x) == 0:
        #     empty.append(job)
    return y
    # return empty
    # return [ ( l, m.group(1) ) for l in list for m in (filter(l),) if m]


def software():
    new_title_list = [tokenize_and_stem(i) for i in job_title]
    searchRegex = re.compile('(io|softwar|develop|thiel|innovation|websit|web|forward|deploy|develop|fullstack|python|java|agil|programm|applic|autopilot|fellow)').search
    x = filterPick(new_title_list, searchRegex, 'software')
    return x

software()

def engineer():
    new_title_list = [tokenize_and_stem(i) for i in job_title]
    # ['mechan', 'industri', 'skule', 'drill', 'robot', 'electr']
    searchRegex = re.compile(
        '(mechan|industri|skule|drill|robot|electr)').search
    x = filterPick(new_title_list, searchRegex, 'engineering')
    return x


def research():
    new_title_list = [tokenize_and_stem(i) for i in job_title]
    searchRegex = re.compile(
        '(research|lectur)').search
    x = filterPick(new_title_list, searchRegex, 'research')
    return x


def design():
    new_title_list = [tokenize_and_stem(i) for i in job_title]
    searchRegex = re.compile(
        '(design)').search
    x = filterPick(new_title_list, searchRegex, 'design')
    return x


def data():
    new_title_list = [tokenize_and_stem(i) for i in job_title]
    searchRegex = re.compile(
        '(data|scien|big data|data vi|data analy|machine learning)').search
    x = filterPick(new_title_list, searchRegex, 'data science')
    return x


def product():
    new_title_list = [tokenize_and_stem(i) for i in job_title]
    searchRegex = re.compile(
        '(product)').search
    x = filterPick(new_title_list, searchRegex, 'product manager')
    return x


def finance():
    new_title_list = [tokenize_and_stem(i) for i in job_title]
    # ['financi', 'account', 'payabl', 'record', 'clerk', 'busi', 'busi', 'develop', 'busi', 'analyst', 'oper', 'logist',
    #  'market', 'busi', 'intellig', 'digit', 'market', 'invest', 'invest', 'bank', 'capit', 'market', 'ventur', 'merger',
    #  'acquisit', 'consult', 'account', 'privat', 'equiti']
    searchRegex = re.compile(
        '(chair|financi|account payabl|record clerk|busi develop|busi|busi analyst|oper|logist|market|busi intellig|digit market|invest|invest bank|capit|capit market|ventur|merger|acquisit|consult|account|privat|equiti|)').search
    x = filterPick(new_title_list, searchRegex, 'business and finance')
    return x


def startup():
    new_title_list = [tokenize_and_stem(i) for i in job_title]
    searchRegex = re.compile(
        '(co-found|founder|presid|chief|execut|offic|vice-presid|cofound)').search
    x = filterPick(new_title_list, searchRegex, 'startup founder')
    return x


def admin_it(): # admin/hr/coordination/it
    new_title_list = [tokenize_and_stem(i) for i in job_title]
    searchRegex = re.compile(
        '(administr|associ|project|assist|coordin|repres|ambassador|teach|talent)').search
    x = filterPick(new_title_list, searchRegex, 'admin/coordination/it')
    return x

# l = ['associate', 'project', 'assistant', 'coordinator', 'associate'
#      'representative', 'ambassador', 'teaching', 'talent']
# print(stem_for_regex(l))

# def temp():
#     new_title_list = [tokenize_and_stem(i) for i in job_title]
#     searchRegex = re.compile(
#         '(io|softwar|develop|thiel|innovation|websit|web|forward|deploy|develop|fullstack|python|java|agil|programm|applic|mechan|industri|skule|drill|robot|electr|research|lectur|design|data|scien|big data|data vi|data analy|machine learning|product|chair|financi|account payabl|record clerk|busi develop|busi|busi analyst|oper|logist|market|busi intellig|digit market|invest|invest bank|capit|capit market|ventur|merger|acquisit|consult|account|privat|equiti|co-found|founder|presid|chief|execut|offic|vice-presid|general partner)').search
#     x = filterPick(new_title_list, searchRegex)
#     return x

# for i in temp():
#     print(i)



def write_to_file(items):
    for i in items:
        if len(i) != 0:
            with open('job_classified', 'a') as f:
                job = ' '.join(i[0][0])
                classification = i[0][1]
                # print(job + ', ' + classification)
                f.write(job + ', ' + classification + '\n')

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


lines = open('job_classified').readlines()
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

# data_count = count(classification)
# barGraph(data_count)


# software = software()
# write_to_file(software)
# finance = finance()
# write_to_file(finance)
# product = product()
# write_to_file(product)
# startup = startup()
# write_to_file(startup)
# data = data()
# write_to_file(data)
# design = design()
# write_to_file(design)
# research = research()
# write_to_file(research)
# engineer = engineer()
# write_to_file(engineer)
# admin = admin_it()
# write_to_file(admin)


import string
from nltk.tag import pos_tag
from gensim import corpora, models, similarities

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
#
# lines = open('job_classified').readlines()
# lines = [line.replace('\n', '') for line in lines]
# job_list, job_class = [], []
# for line in lines:
#     new_line = line.split(', ')
#     job_class.append(new_line[-1])
#     job_list.append(new_line[:-1])


# for i in job_list:
#     print(i)
# print(job_list)
# job_list = [job.split() for job in job_list]
# for i in job_list:
#     print(i)
# vocab = vocabSet(job_list)
# texts = [bag_of_words(vocab, job) for job in job_list]
#
#
# job_list = [i.split() for w in job_list for i in w]
# dictionary = corpora.Dictionary(job_list)
#
#
# # #remove extremes (similar to the min/max df step used when creating the tf-idf matrix)
# dictionary.filter_extremes(no_below=1, no_above=0.8)
# #
# # #convert the dictionary to a bag of words corpus for reference
# corpus = [dictionary.doc2bow(text) for text in job_list]
# #
# lda = models.LdaModel(corpus, num_topics=7,
#                             id2word=dictionary,
#                             update_every=5,
#                             chunksize=10000,
#                             passes=50)
#
# print(lda.show_topics())

# topics_matrix = lda.show_topics(formatted=False, num_words=20)
# print(topics_matrix)




import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor

lines = open('job_classified').readlines()
lines = [line.replace('\n', '') for line in lines]
job_list, job_class = [], []
for line in lines:
    new_line = line.split(', ')
    job_class.append(new_line[-1])
    job_list.append(new_line[:-1])


job_list = [job.split() for job in job_list]

vocab = vocabSet(job_list)
texts = [bag_of_words(vocab, job) for job in job_list]

X_train, X_test, y_train, y_test = train_test_split(texts, job_class)

# Create a random dataset
# rng = np.random.RandomState(1)
# X = np.sort(200 * rng.rand(600, 1) - 100, axis=0)
# y = np.array([np.pi * np.sin(X).ravel(), np.pi * np.cos(X).ravel()]).T
# y += (0.5 - rng.rand(*y.shape))

# X_train, X_test, y_train, y_test = train_test_split(X, y,
#                                                     train_size=400,
#                                                     random_state=4)
#
max_depth = 30
regr_rf = RandomForestRegressor(max_depth=max_depth, random_state=2)
regr_rf.fit(X_train, y_train)
y_rf = regr_rf.predict(X_test)


# regr_multirf = MultiOutputRegressor(RandomForestRegressor(max_depth=max_depth,
#                                                           random_state=0))
# regr_multirf.fit(X_train, y_train)


# Predict on new data
# y_multirf = regr_multirf.predict(X_test)
# y_rf = regr_rf.predict(X_test)












# def strip_proppers(text):
#     # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
#     tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent) if word.islower()]
#     # return tokens
#     # tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent) if word.islower()]
#     return "".join([" "+i if not i.startswith("'") and i not in string.punctuation else i for i in tokens]).strip()
#
#
# def strip_proppers_POS(text):
#     tagged = pos_tag(text.split()) #use NLTK's part of speech tagger
#     non_propernouns = [word for word,pos in tagged if pos != 'NNP' and pos != 'NNPS']
#     return non_propernouns
#
#
# #remove proper names
# preprocess = [strip_proppers(doc) for doc in list_job_title]
#
# #tokenize
# tokenized_text = [tokenize_and_stem(text) for text in preprocess]
#
# # #remove stop words
# texts = [[word for word in text if word not in stopwords] for text in tokenized_text]





















# def tokenize_only(text):
#     # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
#     tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
#     filtered_tokens = []
#     # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
#     for token in tokens:
#         if re.search('[a-zA-Z]', token):
#             filtered_tokens.append(token)
#     return filtered_tokens
#
# list_job_title = get_job_title()
#
# totalvocab_stemmed = []
# totalvocab_tokenized = []
# for i in list_job_title:
#     allwords_stemmed = tokenize_and_stem(i)  # for each item in 'synopses', tokenize/stem
#     totalvocab_stemmed.extend(allwords_stemmed)  # extend the 'totalvocab_stemmed' list
#
#     allwords_tokenized = tokenize_only(i)
#     totalvocab_tokenized.extend(allwords_tokenized)
#
# vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index = totalvocab_stemmed)  # pandas is the shit...
# # print(vocab_frame.head())  # returns first n rows!
#
#
#
#
# #define vectorizer parameters
# tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
#                                  min_df=0.2, stop_words='english',
#                                  use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1,3))
#
# tfidf_matrix = tfidf_vectorizer.fit_transform(list_job_title)  # fit the vectorizer to synopses
#
# # print(tfidf_matrix.shape)
#
# terms = tfidf_vectorizer.get_feature_names()
# dist = 1 - cosine_similarity(tfidf_matrix)
#
# num_clusters = 5
# # km = KMeans(n_clusters=num_clusters)
# # km.fit(tfidf_matrix)
# # clusters = km.labels_.tolist()
#
# # joblib.dump(km,  'doc_cluster.pkl')
#
# km = joblib.load('doc_cluster.pkl')
# clusters = km.labels_.tolist()
#
# total_dict = {'title': list_job_title, 'cluster': clusters}
# frame = pd.DataFrame(total_dict, index = [clusters], columns = ['title', 'cluster'])
# # print(frame['cluster'].value_counts())
#
#
# import os  # for os.path.basename
#
# import matplotlib.pyplot as plt
# import matplotlib as mpl
#
# from sklearn.manifold import MDS
#
# MDS()
#
# # convert two components as we're plotting points in a two-dimensional plane
# # "precomputed" because we provide a distance matrix
# # we will also specify `random_state` so the plot is reproducible.
# mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
#
# pos = mds.fit_transform(dist)  # shape (n_components, n_samples)
#
# xs, ys = pos[:, 0], pos[:, 1]
# print()
# print()
#
# #set up colors per clusters using a dict
# cluster_colors = {0: '#1b9e77', 1: '#d95f02', 2: '#7570b3', 3: '#e7298a', 4: '#66a61e'}
#
# #set up cluster names using a dict
# cluster_names = {0: 'Family, home, war',
#                  1: 'Police, killed, murders',
#                  2: 'Father, New York, brothers',
#                  3: 'Dance, singing, love',
#                  4: 'Killed, soldiers, captain'}
#
# df = pd.DataFrame(dict(x=xs, y=ys, label=clusters, title=list_job_title))
#
# # group by cluster
# groups = df.groupby('label')
#
# # set up plot
# fig, ax = plt.subplots(figsize=(17, 9))  # set size
# ax.margins(0.05)  # Optional, just adds 5% padding to the autoscaling
#
# # iterate through groups to layer the plot
# # note that I use the cluster_name and cluster_color dicts with the 'name' lookup to return the appropriate color/label
# for name, group in groups:
#     ax.plot(group.x, group.y, marker='o', linestyle='', ms=12,
#             label=cluster_names[name], color=cluster_colors[name],
#             mec='none')
#     ax.set_aspect('auto')
#     ax.tick_params( \
#         axis='x',  # changes apply to the x-axis
#         which='both',  # both major and minor ticks are affected
#         bottom='off',  # ticks along the bottom edge are off
#         top='off',  # ticks along the top edge are off
#         labelbottom='off')
#     ax.tick_params( \
#         axis='y',  # changes apply to the y-axis
#         which='both',  # both major and minor ticks are affected
#         left='off',  # ticks along the bottom edge are off
#         top='off',  # ticks along the top edge are off
#         labelleft='off')
#
# ax.legend(numpoints=1)  # show legend with only 1 point
#
# # add label in x,y position with the label as the film title
# for i in range(len(df)):
#     ax.text(df.ix[i]['x'], df.ix[i]['y'], df.ix[i]['title'], size=8)
#
# # plt.show()  # show the plot
#
#
# #define custom toolbar location
# class TopToolbar(mpld3.plugins.PluginBase):
#     """Plugin for moving toolbar to top of figure"""
#
#     JAVASCRIPT = """
#     mpld3.register_plugin("toptoolbar", TopToolbar);
#     TopToolbar.prototype = Object.create(mpld3.Plugin.prototype);
#     TopToolbar.prototype.constructor = TopToolbar;
#     function TopToolbar(fig, props){
#         mpld3.Plugin.call(this, fig, props);
#     };
#
#     TopToolbar.prototype.draw = function(){
#       // the toolbar svg doesn't exist
#       // yet, so first draw it
#       this.fig.toolbar.draw();
#
#       // then change the y position to be
#       // at the top of the figure
#       this.fig.toolbar.toolbar.attr("x", 150);
#       this.fig.toolbar.toolbar.attr("y", 400);
#
#       // then remove the draw function,
#       // so that it is not called again
#       this.fig.toolbar.draw = function() {}
#     }
#     """
#     def __init__(self):
#         self.dict_ = {"type": "toptoolbar"}
#
# # create data frame that has the result of the MDS plus the cluster numbers and titles
# df = pd.DataFrame(dict(x=xs, y=ys, label=clusters, title=list_job_title))
#
# # group by cluster
# groups = df.groupby('label')
#
# # define custom css to format the font and to remove the axis labeling
# css = """
# text.mpld3-text, div.mpld3-tooltip {
#   font-family:Arial, Helvetica, sans-serif;
# }
#
# g.mpld3-xaxis, g.mpld3-yaxis {
# display: none; }
#
# svg.mpld3-figure {
# margin-left: -200px;}
# """
#
# # Plot
# fig, ax = plt.subplots(figsize=(14, 6))  # set plot size
# ax.margins(0.03)  # Optional, just adds 5% padding to the autoscaling
#
# # iterate through groups to layer the plot
# # note that I use the cluster_name and cluster_color dicts with the 'name' lookup to return the appropriate color/label
# for name, group in groups:
#     points = ax.plot(group.x, group.y, marker='o', linestyle='', ms=18,
#                      label=cluster_names[name], mec='none',
#                      color=cluster_colors[name])
#     ax.set_aspect('auto')
#     labels = [i for i in group.title]
#
#     # set tooltip using points, labels and the already defined 'css'
#     tooltip = mpld3.plugins.PointHTMLTooltip(points[0], labels,
#                                              voffset=10, hoffset=10, css=css)
#     # connect tooltip to fig
#     mpld3.plugins.connect(fig, tooltip, TopToolbar())
#
#     # set tick marks as blank
#     ax.axes.get_xaxis().set_ticks([])
#     ax.axes.get_yaxis().set_ticks([])
#
#     # set axis as blank
#     ax.axes.get_xaxis().set_visible(False)
#     ax.axes.get_yaxis().set_visible(False)
#
# ax.legend(numpoints=1)  # show legend with only one dot
#
# mpld3.show()
# html = mpld3.fig_to_html(fig)
# print(html)


# print("Top terms per cluster:")
# print()
# # sort cluster centers by proximity to centroid
# order_centroids = km.cluster_centers_.argsort()[:, ::-1]
#
# for i in range(num_clusters):
#     print("Cluster %d words:" % i, end='')
#
#     for ind in order_centroids[i, :6]:  # replace 6 with n words per cluster
#         print(' %s' % vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore'), end=',')
#     print()  # add whitespace
#     print()  # add whitespace
#
#     print("Cluster %d titles:" % i, end='')
#     for title in frame.ix[i]['title'].values.tolist():
#         print(' %s,' % title, end='')
#     print()  # add whitespace
#     print()  # add whitespace
#
# print()
# print()

# import string
#
#
# def strip_proppers(text):
#     # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
#     tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent) if word.islower()]
#     # return tokens
#     # tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent) if word.islower()]
#     return "".join([" "+i if not i.startswith("'") and i not in string.punctuation else i for i in tokens]).strip()
#
#
# from nltk.tag import pos_tag
#
# def strip_proppers_POS(text):
#     tagged = pos_tag(text.split()) #use NLTK's part of speech tagger
#     non_propernouns = [word for word,pos in tagged if pos != 'NNP' and pos != 'NNPS']
#     return non_propernouns
#
#
# from gensim import corpora, models, similarities
#
# #remove proper names
# preprocess = [strip_proppers(doc) for doc in list_job_title]
#
# #tokenize
# tokenized_text = [tokenize_and_stem(text) for text in preprocess]
#
# # #remove stop words
# texts = [[word for word in text if word not in stopwords] for text in tokenized_text]

# for i in texts:
#     print(i)
#create a Gensim dictionary from the texts
# dictionary = corpora.Dictionary(texts)


# #remove extremes (similar to the min/max df step used when creating the tf-idf matrix)
# dictionary.filter_extremes(no_below=1, no_above=0.8)
#
# #convert the dictionary to a bag of words corpus for reference
# corpus = [dictionary.doc2bow(text) for text in texts]
#
# lda = models.LdaModel(corpus, num_topics=6,
#                             id2word=dictionary,
#                             update_every=5,
#                             chunksize=10000,
#                             passes=100)
#
# # print(lda.show_topics())
#
# topics_matrix = lda.show_topics(formatted=False, num_words=20)
# print(topics_matrix)
