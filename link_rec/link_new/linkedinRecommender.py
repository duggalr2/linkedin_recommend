import random, pickle
from preprocess_text import TextProcessing
from file_handler import FileProcessor
from cosine_similarity import CosineSimilarity


############################################
# Linkedin Recommender System:
# - Decided to have rating on education, experience  and overall (exp+edu)
# - It will make the Recommender more accurate
############################################

def common_profile_stop_words(item):
    """
    Remove's common noisy words found in linkedin profiles
    """
    noise_words = [
        'Field', 'Of', 'Study', 'Degree', 'Name',
    ]
    return [i for i in item if i not in noise_words]


def get_education(item):
    """ Return's clean list of education """
    edu = item.get('education')
    edu = [t.tokenize(i) for i in edu]
    edu = [i for y in edu for i in y]
    edu = t.remove_punctuation_list(edu)
    edu = t.remove_stop_words_list(edu)
    return common_profile_stop_words(edu)


def get_experience(item):
    """ Return's clean list of experience """
    exp = item.get('experience')
    exp = t.remove_punctuation_list(exp)
    exp = t.remove_stop_words_list(exp)
    return exp


def get_header(item):
    """ Return's clean list of header """
    header = item.get('header')
    header = t.remove_punctuation_list(header)
    header = t.remove_stop_words_list(header)
    return header


def duplicate(filename1, filename2, type_file):
    """
    Return's a list of duplicates in byte file
    """
    # TODO: This code is terrible!
    if type_file == 'byte':
        items_file1 = FileProcessor(filename1, 'train')
        items_file2 = FileProcessor(filename2, 'train')
        items_file1 = items_file1.readByteFile()
        items_file2 = items_file2.readByteFile()
        # items_file1 = [item for item in items_file1 if item != '\n' and item != None]
        # items_file2 = [item for item in items_file2 if item != '\n' and item != None]
        return [item for item in items_file2 if item in items_file1]
        # return duplicate_list
    elif type_file == 'txt':
        items_file1 = FileProcessor(filename1, 'train')
        items_file2 = FileProcessor(filename2, 'train')
        items_file1 = items_file1.readFile()
        items_file2 = items_file2.readFile()
        # items_file1 = [item for item in items_file1 if item != '\n' and item != None]
        # items_file2 = [item for item in items_file2 if item != '\n' and item != None]
        return [item for item in items_file2 if item in items_file1]
        # return duplicate_list
    else:
        return 'Only byte or txt'


def rating_prompt(items, filename1, filename2, num=10):
    """
    Ask's the user questions about what they would rate certain profiles;
    Allow's the recommender system to understand what type of profiles user likes
    Parameters:
        -items: list of dictionaries with education, experience, and header <-- should be the readByteFile items
        -filename1: name of file or path where the original items are stored
        -filename2: name of file or path where the rated items will be stored
    """
    # assert type(items) == dict
    new_list = []
    num = [random.randrange(0, len(items)-1) for i in range(num)]
    duplicate_list = duplicate(filename1, filename2, 'txt')
    for i in num:
        if i not in duplicate_list:
            # with open(filename1, 'w') as b:
            #     b.write()
            education = items[i].get('education')
            print('Education: ', education)
            rating_education = int(input('Enter rating for education (1 to 5): '))
            if rating_education > 5:
                raise Exception('Rating must be 5 or less wtf..')
            experience = items[i].get('experience')
            print('Experience: ', experience)
            rating_experience = int(input('Enter rating for experience (1 to 5): '))
            if rating_experience > 5:
                raise Exception('Rating must be 5 or less wtf..')
            items[i]['rating'] = [rating_education, rating_experience, (rating_education+rating_experience)]
            new_list.append(items[i])
        else:
            pass

    with open(filename2, 'ab') as b:
        for i in new_list:
            pickle.dump(i, b)
            pickle.dump('\n', b)

    print('Done!')


def get_ratings(filename):
    """
    Return's a list of ratings
    Parameters:
        -filename: name of file or path where the rated items will be stored
    """
    f = FileProcessor(filename, 'train')
    lines = f.readByteFile()
    lines = [line for line in lines if line != '\n' and line != None]
    return [line.get('rating') for line in lines]


def calculate_rating_url(url, ratings, wordVectors, vocabSet, alg=0):
    """
    """
    pass


def calculate_rating_dict(line, ratings, wordVectors, vocabSet, alg=0):
    """
    (To get best results, make sure you are consistent with the algoirthm choice
    ie. If wordVectors is using tf-idf3 weight, the title should also be using the same weighting...)
    Calculate's Rating of a Book;
    Parameter: -Line (what you want to get the rating of) must a be list
               -Ratings: List of get ratings function
               -Bag of Words: from bag of words function
               -Vocab Set: from vocabSet function
               -alg: default is bag of words using no tf-idf weighting
    """
    assert type(line) == dict
    edu = get_education(line)
    exp = get_experience(line)
    final_list = []
    final_list.append(edu)
    final_list.append(exp)

    t1 = [c.bag_of_words(vocabSet, i) for i in final_list]
    education_vector = t1[0]
    # experience_vector = t1[1]

    # if alg == 1:
    #     t1 = c.tf_idf1(t1, vocabSet)
    # elif alg == 2:
    #     t1 = c.tf_idf2(t1, vocabSet)
    # elif alg == 3:
    #     t1 = c.tf_idf3(t1, vocabSet)

    w = [c.cosine_similarity(i, education_vector) for i in wordVectors]
    for i in w:
        if type(i) == str:
            ind = w.index(i)
            w[ind] = 0
            # return 'With our data, I cannot come up with a rating...'

    assert len(w) == len(ratings)
    print(line.get('education'))
    y = [w[i] * ratings[i][1] for i in range(len(ratings))]
    return sum(y) / sum(w)


def test_recommender():
    """
    """
    pass


def recommend():
    """
    """
    pass


if __name__ == '__main__':
    t = TextProcessing()
    c = CosineSimilarity()
    byte_file_path = '/Users/Rahul/Desktop/Main/Side_projects/project_2/lifeline/Scripts/link_new/files/linkedin_people_description'
    byte_file = FileProcessor(byte_file_path, 'train')
    items = byte_file.readByteFile()
    items = [item for item in items if item != '\n' and item != None]

    # big_list = [] # education + experience list
    # for i in items:
    #     print(i)
    #     edu = get_education(i)
    #     exp = get_experience(i)
    #     big_list.append(edu)
    #     big_list.append(exp)
    #
    # vocabSet = c.vocabSet(big_list)
    # wordVectors = [c.bag_of_words(vocabSet, i) for i in big_list]

    ratings_file_path = '/Users/Rahul/Desktop/Main/Side_projects/project_2/lifeline/Scripts/link_new/files/linkedin_rating_backend'
    ratings_file = FileProcessor(ratings_file_path, 'train')
    ratings = ratings_file.readByteFile()
    ratings = [i for i in ratings if i != '\n' and i != None]

    big_list = []
    r = []
    for i in ratings:
        edu = get_education(i)
        # exp = get_experience(i)
        rat = i.get('rating')
        big_list.append(edu)
        # big_list.append(exp)
        r.append(rat)

    vocabSet = c.vocabSet(big_list)
    wordVectors = [c.bag_of_words(vocabSet, i) for i in big_list]
    # print(calculate_rating_dict(items[4], r, wordVectors, vocabSet))





    # duplicate(byte_file_path, ratings_file_path)
    # li = [
    #     {'education': ['University of Waterloo', 'Degree Name', 'BCS', 'Field Of Study', 'Computer Science'], 'rating': [5, 5, 10], 'experience': ['Software Engineering Intern', 'MemSQL'], 'header': ['Jacob Jackson', '--', 'https://www.linkedin.com/in/jacobbfjackson/']},
    #     {'education': ['University of Toronto', 'Degree Name', 'PhD', 'Field Of Study', 'Computer Science'], 'rating': [4, 2, 6], 'experience': ['Lecturer', 'University of Toronto', 'Research Assistant', 'University of Toronto', 'Teaching Assistant', 'University of Toronto', 'Summer Intern', 'Greenplum', 'Teaching Assistant', 'University of Toronto'], 'header': ['Bogdan Simion', 'Lecturer at University of Toronto', 'https://www.linkedin.com/in/bogdan-simion-1113b27/']}
    # ]
    # with open(byte_file_path, 'ab') as f:
    #     for i in li:
    #         pickle.dump(i, f)
    #         pickle.dump('\n', f)
    # get_ratings(ratings_file_path)

    # edu = get_education(items[1])
    # print(edu)

    # exp = get_experience(items[1])
    # li = []
    # li.append(edu)
    # li.append(exp)
    # print(li)
