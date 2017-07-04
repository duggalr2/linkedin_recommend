from main import *
from linkedin_file import *
import matplotlib.pyplot as plt
from cosine_similarity import CosineSimilarity
from kNN import classify
import numpy as np
import string

############################################################
        # Graphing the Linkedin Description Data
############################################################
# TODO: Nothing in Graph.py works right now since it used the old text processing file
# TODO: make the graphing functions more abstract so it could work for future projects...
# TODO: Fix up all the docstrings
# TODO: transfer all of this file shit to linkedin file....
############################################################################################################

def count(data):
    """
    Return's a dict with key (item) and number of times it appears in list
    """
    main_di = {}
    for i in data:
        if i in main_di:
            main_di[i] += 1
        else:
            main_di[i] = 1
    return main_di

def education_data(org_data):
    """
    Return's list of all the university name's and degree name
    """
    university_name = [i.get('education')[0] for i in org_data]
    degree = []
    for i in org_data:
        x = i.get('education')
        if 'Field Of Study' in x:
            y = x.index('Field Of Study')
            degree.append(x[y+1])
    return university_name, degree

translator = str.maketrans('', '', string.punctuation)

def experience_data(org_data, unclassified_file):
    """
    Return's list of experience and company name
    """
    experience = [i.get('experience')[0].lower() for i in org_data if len(i.get('experience')) >= 2]
    company = [i.get('experience')[1].lower() for i in org_data if len(i.get('experience')) >= 2]
    experience = [i.translate(translator) for i in experience]
    company = [i.translate(translator) for i in company]
    return experience, company

def write_to_file(filename, data):
    """
    (Should be mainly used for writing unclassified labels to specific files and then applying classification...)
    Write's the data to a file; Data must be a 1D list
    """
    assert type(data) == list
    f = open(filename)
    if len(f.readlines()) > 0:
        try:
            s = str(input('There seems to be stuff in the file, should I overwrite it or append (w/a): '))
        except:
            raise Exception('Must be either character "w" or "a"')

        if s == 'w':
            y = input('Okay, I am about to overwrite the file.. this cannot be undone... (Press Enter): ')

        with open(filename, s) as b:
            for i in data:
                b.write(i + '\n')
    else:
        with open(filename, 'a') as b:
            for i in data:
                b.write(i + '\n')

    print('Done')

def parse_classified(filename='experience_classification'):
    """
    Used for parsing a classified file
    """
    f = open(filename)
    lines = f.readlines()
    lines = [line.replace('\n', '').split() for line in lines]
    labels = [line[-1] for line in lines]
    data = [line[:-1] for line in lines]
    return data, labels

# TODO: Make sure this is abstract because degree_name and future info is going through this classification as well!
# TODO: Assert shit...
# TODO: Are capitalize letters being dealt the same?
def classification(data, classified_file, unclassified_file):
    """
    Classifying the unclassified experience labels (will be especially useful for future as data grows...)
    Parameter: -Data: experience data
               -Classified_file: experience with labels
               -Unclassified_file: experience without labels
    """
    f = open(unclassified_file)
    lines = f.readlines()
    lines = [line.replace('\n', '') for line in lines]
    data, labels = parse_classified()
    vocabSet = c.vocabSet(data)
    bagOfWords = [c.bag_of_words(vocabSet, i) for i in data]
    errCount = 0
    for i in range(len(bagOfWords)):
        x = classify(np.array(bagOfWords[i]), np.array(bagOfWords), labels, 20)
        print(data[i], x, labels[i])
        if x != labels[i]: errCount+=1
    print(errCount/len(bagOfWords))

    # TODO: run that through SVM (according to RP, its the best one)
    # TODO: THOUGHT: after done SVM, write all the classified ones to current classification file
                        # TODO: (want all of them there to graph!)


def pie_graph(data_count):
    """
    Graph's a pie graph of the data with count values (only shows schools that appear more than once)
    Parameter: -data_count: dict
    """
    names, count = [], []
    for val, key in data_count.items():
        if key > 1:
            names.append(val)
            count.append(key)

    fig1, ax1 = plt.subplots()
    ax1.pie(count, labels=names, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    original_data = read_byteFile(
        '/Users/Rahul/Desktop/Main/Side_projects/project_2/lifeline/Scripts/link_new/files/linkedin_people_description')
    original_data = [i for i in original_data if i != '\n' and i != None]
    edu, degree = education_data(original_data)
    edu_dict = count(edu)
    pie_graph(edu_dict)
    c = CosineSimilarity()
    # experience, company = experience_data(original_data, 'experience_unclassified')
    # classification(experience, 'experience_classification', 'experience_unclassified')



    ######################################################
    # TODO: transfer all of this file shit to linkedin file....
    ######################################################
    # write_to_file('experience_unclassified', experience)
