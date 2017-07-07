import linkedin_parser
import sqlite3

####
# Personal Linkedin Function to fill up database with profiles....
####



def open_file(filename):
    f = open(filename)
    lines = f.readlines()
    lines = [line.replace('\n', '') for line in lines if len(line)>1]
    return lines

linkedin = linkedin_parser.Linkedin()
linkedin.linkedin_login()
lines = open_file('linkedin_dest_url')
print(linkedin.get_person_information('https://www.linkedin.com/in/rahul-duggal-402506134/'))


def dump_profiles(num_iter):
    while num_iter >= 1:
        new_list = []
        lines = open_file('linkedin_dest_url')
        for line in lines:
            list_url = linkedin.get_people_viewed(line)
            new_list.append(list_url)
        num_iter -= 1
        new_list = list(set([y for i in new_list for y in i]))
        with open('linkedin_dest_url', 'w') as f:
            for i in new_list:
                f.write(i + '\n')
        print('Done', num_iter)
    print('DONE')

#dump_profiles(2)


def parse_profiles_to_db(filename):
    conn = sqlite3.connect('/Users/Rahul/Desktop/Main/Side_projects/linkedin_recommend/db.sqlite3')
    c = conn.cursor()
    #c.execute('SELECT * FROM link_rec_profile')
    c.execute('SELECT * FROM link_rec_parsedprofile')
    y = c.fetchall()

parse_profiles_to_db('linkedin_dest_url')



