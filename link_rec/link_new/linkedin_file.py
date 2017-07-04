from linkedinRecommender import duplicate
from linkedin_parser import Linkedin
import pickle, random
from timeit import default_timer as timer
from file_handler import FileProcessor

##############################################################
    # Handling all file stuff for LinkedIn Script
##############################################################

# print(duplicate('/Users/Rahul/Desktop/Main/Side_projects/project_2/lifeline/Scripts/link_new/files/linkedin_raw_url',
#                 '/Users/Rahul/Desktop/Main/Side_projects/project_2/lifeline/Scripts/link_new/files/linkedin_dest_url', 'txt'))


def description_duplicate_url_checker(url):
    """
    Check's if urls in raw_url file are not already in the link_people_description file
    """
    f = FileProcessor(
        '/Users/Rahul/Desktop/Main/Side_projects/project_2/lifeline/Scripts/link_new/files/linkedin_people_description',
        'train')
    items = f.readByteFile()
    li = [i for i in items if i != '\n' and i != None]
    for i in li:
        link = i.get('header')[-1]
        if url == link:
            return True
    return False


def get_more_urls(org_file, dest_file, num=0):
    """
    Transfer's all url's from the raw_url file (same as the js file) to a new file with 10+ viewed people
    Deletes all the url's transferfed from the original file
    Parameters: -Org_file: Initial Raw Url File
                -Dest_File: New File you want this to be transferred
                -Num default will be to get all the urls in the original raw file
    """

    li = duplicate('/Users/Rahul/Desktop/Main/Side_projects/project_2/lifeline/Scripts/link_new/files/linkedin_raw_url',
                   '/Users/Rahul/Desktop/Main/Side_projects/project_2/lifeline/Scripts/link_new/files/linkedin_dest_url',
                   'txt')

    f = FileProcessor(org_file, 'train')
    lines = f.readFile()
    lines = [line.replace('\n', '') for line in lines if line not in li]
    f.eraseFile()



    # lines = list(set(lines))  # list of unique urls only
    # lines = [i for i in lines if description_duplicate_url_checker(i) != True]  # removes all url's that already exist
    #
    # with open(dest_file, 'a') as b:
    #     if num == 0:
    #         num = len(lines)
    #     assert len(lines) >= num
    #     for i in range(num):
    #         li = linkedin_parser.get_people_viewed(lines[i])
    #         for y in li:
    #             b.write(y + '\n')
    #
    # # TODO: DON'T KNOW IF THIS IS THE MOST EFFICIENT WAY TO DO THIS..
    # with open(org_file, 'w') as c:
    #     for i in range(num, len(lines)):
    #         c.write(lines[i] + '\n')
    #
    # print('Done!')


def get_main_description(filename, new_file, num=10):
    """
    Get's the main description from the urls in filename (should be dest_file) and writes to new_file
    Parameter -num: used to determine how many random index will be chosen; default will be 10 or specify otherwise
        Note: num should be 20 or less for script to run smoothly;
        (network can slow down or JS might not properly render if more...)
    """
    f = open(filename, 'r+')
    lines = f.readlines()
    lines = [line.replace('\n', '') for line in lines]
    lines = list(set(lines))  # remove all duplicates..
    lines = [i for i in lines if description_duplicate_url_checker(i) != True]
    assert len(lines) >= num
    with open(new_file, 'ab') as b:
        for i in range(num):
            random_index = random.randrange(len(lines) - 1)
            di = linkedin_parser.get_person_information(lines[random_index])
            pickle.dump(di, b)
            pickle.dump('\n', b)
            del lines[random_index]
            f.seek(0)
            f.truncate()
            for line in lines:
                f.write(line + '\n')
    print('Done!')


# TODO: change filename to backend filename... add rating of edu/exp
# TODO: double check this function to see if it works
def rating_prompt(original_data, filename='linkedin_rating_backend'):
    """
    (Couldn't use the original rating prompt because dealing with dictionaries)
    (Really only used once in the beginning...)
    Rating Prompt allowing me to originally rate people for recommender system...
    Parameter: -original_data: list of parsed and clean dictionaries
               -filename: the file where the dictionaries are located
            rating = [edu, exp, total]
    """
    li = []
    for i in original_data:
        print(i)
        edu = int(input('Enter a rating of education (based on title, 1 to 5): '))
        exp = int(input('Enter a rating of experience (based on title, 1 to 5): '))
        total = edu + exp
        i['rating'] = [edu, exp, total]
        li.append(i)  # new dictionaries

    f = FileProcessor(filename, 'train')
    f.eraseFile()
    # erase_file(filename)
    with open(filename, 'ab') as b:
        for i in li:
            pickle.dump(i, b)
            pickle.dump('\n', b)

    print('Done!')


if __name__ == '__main__':
    linkedin_parser = Linkedin()
    # linkedin_parser.linkedin_login()

    get_more_urls('/Users/Rahul/Desktop/Main/Side_projects/project_2/lifeline/Scripts/link_new/files/linkedin_raw_url',
                  '/Users/Rahul/Desktop/Main/Side_projects/project_2/lifeline/Scripts/link_new/files/linkedin_dest_url',
                  num=10)
    # get_main_description(
    #     '/Users/Rahul/Desktop/Main/Side_projects/project_2/lifeline/Scripts/link_new/files/linkedin_dest_url',
    #     '/Users/Rahul/Desktop/Main/Side_projects/project_2/lifeline/Scripts/link_new/files/linkedin_people_description',
    #     num=10)


    # erase_file('/Users/Rahul/Desktop/Main/Side_projects/project_2/lifeline/Scripts/link_new/files/linkedin_people_description')
    # items = read_byteFile('/Users/Rahul/Desktop/Main/Side_projects/project_2/lifeline/Scripts/link_new/files/linkedin_people_description')
    # li = [i for i in items if i != '\n' and i != None] # None is if JS didn't get rendered and profile didn't load (rare)
    # for i in li:
    #     print(i)
    # print(len(li))
    # rating_prompt(li)
    # ratings = read_byteFile('/Users/Rahul/Desktop/Main/Side_projects/project_2/lifeline/Scripts/link_new/files/linkedin_rating_backend')
    # ratings = [i for i in ratings if i != '\n']
