from file_handler import FileProcessor
from preprocess_text import TextProcessing
import matplotlib.pyplot as plt

#######################################################################################
# Graphing Linkedin: Education, Experience: Companies and Categories
#######################################################################################

# TODO: To generate more accurate graphs, look at the data for each category and see if there are words I can
# i.e. Experience will make a lot more sense when it is classified
# TODO: remove or generalize to make the graphs more accurate
# TODO: Again, it doesn't make a significant difference so do it after recommender system is done!

def clean_data(data):
    """
    Remove's all punctuation and lowercase all items in a list
    """
    data = t.remove_punctuation_list(data)
    data = t.lower_text_in_list(data)
    return data


def get_education_data(items):
    """
    Return's list of all the university name's and degree name
    """
    university_name = []
    degree = []
    for i in items:
        education = i.get('education')
        if 'Field Of Study' in education:
            y = education.index('Field Of Study')
            degree.append(education[y + 1])
        uni_name = education[0]
        university_name.append(uni_name)
    return university_name, degree


def get_experience_data(items):
    """
    Return's list of experience and company name
    """
    experience = [i.get('experience')[0].lower() for i in items if len(i.get('experience')) >= 2]
    company = [i.get('experience')[1].lower() for i in items if len(i.get('experience')) >= 2]
    return experience, company


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


def pieGraph(data_count):
    """
    Graph's a pie graph of the data with count values; Only includes data that appears more than once!
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


def multiplePieGraph():
    """
    Show's all the Pie Graph's at once
    """
    pass


if __name__ == '__main__':
    t = TextProcessing()
    byte_file = FileProcessor(
        '/Users/Rahul/Desktop/Main/Side_projects/project_2/lifeline/Scripts/link_new/files/linkedin_people_description',
        'train')
    items = byte_file.readByteFile()
    items = [item for item in items if item != '\n' and item != None]


    # uni_name, degree_name = get_education_data(items)
    # experience, company_name = get_experience_data(items)
    # uni_name, degree_name = clean_data(uni_name), clean_data(degree_name)
    # experience, company_name = clean_data(experience), clean_data(company_name)

    # uni_name_count, degree_name_count, experience_count, company_name_count = count(uni_name), count(
    #     degree_name), count(experience), count(company_name)
    #
    # for i in degree_name: # split the dual degree
    #     if 'and' in i:
    #         and_index = i.index('and')
    #         d1 = i[:and_index]
    #         d2 = i[and_index+len('and')+1:]
    #         degree_name.append(d1)
    #         degree_name.append(d2)
    #         degree_name.remove(i)

    # pieGraph(degree_name_count)

    # for i in degree_name_count:
    #     print(i, degree_name_count[i])


# University Name:
    # - It's mainly good except that trinity college one should be under uoft so fix that!

# Degree Name:
    # - Definitely needs some work

# Company Name:
    # - Not as much work as degree work but similar problem to degree/uni names (ie. snap vs snapchat)
