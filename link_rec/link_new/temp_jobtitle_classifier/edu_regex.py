import sqlite3
import nltk
from nltk.stem.snowball import SnowballStemmer
import re


def get_education():
    conn = sqlite3.connect('/Users/Rahul/Desktop/Main/Side_projects/linkedin_recommend/db.sqlite3')
    c = conn.cursor()
    c.execute('SELECT school_program FROM link_rec_allparsedprofile')
    y = c.fetchall()
    c.execute('SELECT school FROM link_rec_allparsedprofile')
    w = c.fetchall()
    return [i[0] for i in y if i[0] is not None], [i[0] for i in w if i[0] is not None]

education_list, school_list = get_education()


stopwords = nltk.corpus.stopwords.words('english')  # load the stop words from nltk
stemmer = SnowballStemmer("english")  # stemming


def tokenize_and_stem(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            if 'and' == token:
                token = ''
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens if len(t) > 0]
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
    x = filterPick(new_title_list, searchRegex, '0')
    return x


def finance():
    new_title_list = [tokenize_and_stem(i) for i in education_list]
    searchRegex = re.compile('(financ|commerc|busi|manag|account|market)').search
    x = filterPick(new_title_list, searchRegex, '1')
    return x


def engineer():
    new_title_list = [tokenize_and_stem(i) for i in education_list]
    searchRegex = re.compile('(mechan|engi|aerospac|electr|robot|bioengin|civil|mechatron|chemic)').search
    x = filterPick(new_title_list, searchRegex, '2')
    return x


def math_sciences():
    new_title_list = [tokenize_and_stem(i) for i in education_list]
    searchRegex = re.compile('(mathemat|math|physic|statist)').search
    x = filterPick(new_title_list, searchRegex, '3')
    return x


def humanties_lifesci():
    new_title_list = [tokenize_and_stem(i) for i in education_list]
    searchRegex = re.compile('(polit|biolog|psycholog|neurosci|nurs)').search
    x = filterPick(new_title_list, searchRegex, '4')
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






