import pickle
import nltk

# f = pickle.loads(open('linkedin_people_description', 'rb'))
# print(f)


def readByteFile(filename):
    """
    Read any Byte File;
    """
    b = []
    with open(filename, 'rb') as f:
        while True:
            try:
                b.append(pickle.load(f))  # think this way should work best
            except EOFError:
                break
    return [line for line in b if line != '\n' and line != None]


def get_education_data(items):
    """
    Return's list of all the university name's and degree name
    """
    university_name = []
    degree = None
    uni_name = None
    for i in items:
        education = i.get('education')
        if 'Field Of Study' in education:
            y = education.index('Field Of Study')
            # degree.append(education[y + 1])
            degree = education[y + 1]
        uni_name = education[0]
        # university_name.append(uni_name)
    return uni_name, degree


def classify_education():
    pass


if __name__ == '__main__':
#     parsed_profiles = readByteFile('linkedin_people_description')
#     name, degree = get_education_data(parsed_profiles)
    i = [{'header': ['Rahul Duggal', 'Student at University of Toronto', 'https://www.linkedin.com/in/rahul-duggal-402506134/'], 'education': ['University of Toronto'], 'experience': []}]
    name, deg = get_education_data(i)
    print(name, deg)
    # for i in name:
    #     print(i)