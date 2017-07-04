from junk.clean_the_text import convert_key, remove_filler_words
from linkedin_file import read_byteFile


############################################################################################
# Linkedin Recommender System:
# Recommend's based on education, work experience, and header (not name/url ofc)
############################################################################################

# TODO: Nothing in main works since it used old clean text

# TODO: You login in, if first time, create username/password (store it), it will create files(raw/dest/etc.) for username
# TODO: -Then it will have instructions on where to get started, give an example, have example urls!
# TODO: -Then main will be the interface that the user has access to;

# TODO: (FUTURE) REALLY IMPT: Add functionality for this to also work with csv files! (instead of txt for raw urls, etc)

def get_info_of_url(url):
    """
    Return's rating of person with dictionary, save's person in linkedin_people_description file
    Parameter: -url: linkedin parameter, checks first if url is already in the txt file
    """
    pass

def header_clean_row(row_of_data):
    """
    Return's a clean header row of a specific person
    """
    header = row_of_data.get('header')[1]
    z = list(set(remove_filler_words([header])))
    return z

def education_clean_row(row_of_data):
    """
        Return's a clean education row of a specific person
        """
    education = row_of_data.get('education')
    z = list(set(remove_filler_words(education)))
    return z

def experience_clean_row(row_of_data):
    """
    Return's a clean experience row of a specific person
    """
    experience = row_of_data.get('experience')
    z = list(set(remove_filler_words(experience)))
    return z

def clean_dict_row(original_iterms):
    reList = []
    for row_of_data in original_iterms:
        header = header_clean_row(row_of_data)
        experience = experience_clean_row(row_of_data)
        education = education_clean_row(row_of_data)
        reList.append(header)
        reList.append(experience)
        reList.append(education)
    return reList

def generate_vocabSet(original_data):
    """
    (Could have used the cosine similarity vocabSet function but this is faster...)
    Return's Vocab Set with clean data of header/education/experience
    Parameter: -original_data: must be a dict; should be from read_main_description_file (linkedin_file.py)
    """
    education = convert_key(original_data, 'education')
    experience = convert_key(original_data, 'experience')
    header = convert_key(original_data, 'header')
    vocabSet = []
    vocabSet.append(education)
    vocabSet.append(experience)
    vocabSet.append(header)
    vocabSet = [y for i in vocabSet for y in i]
    vocabSet = list(set(vocabSet))
    return vocabSet

if __name__ == '__main__':
#     c = CosineSimilarity()
    org_items = read_byteFile('linkedin_people_description')
    org_items = [i for i in org_items if i != '\n' and i != None]  # list of parsed dictionaries
#     vocabSet = generate_vocabSet(org_items)
#     education_wordVectors = [c.bag_of_words(vocabSet, education_clean_row(i)) for i in org_items]
#     experience_wordVectors = [c.bag_of_words(vocabSet, experience_clean_row(i)) for i in org_items]
#     header_wordVectors = [c.bag_of_words(vocabSet, header_clean_row(i)) for i in org_items]
#
#     ### Bottom are the good wordVectors (tf-idf variation applied) ###
#
#     education_wordVectors = c.tf_idf3(education_wordVectors, vocabSet)
#     experience_wordVectors = c.tf_idf3(experience_wordVectors, vocabSet)
#     header_wordVectors = c.tf_idf3(header_wordVectors, vocabSet)




