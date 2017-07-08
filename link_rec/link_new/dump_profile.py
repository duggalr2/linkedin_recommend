import linkedin_parser
import sqlite3

####
# Personal Linkedin Function to fill up database with profiles....
####



def open_file(filename):
    f = open(filename)
    lines = f.readlines()
   # print(lines)
    return [line.replace('\n', '') for line in lines if len(line)>1]

linkedin = linkedin_parser.Linkedin()
linkedin.linkedin_login()
#lines = open_file('linkedin_dest_url')
#print(linkedin.get_person_information('https://www.linkedin.com/in/henryhykim/'))


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

#import pickle


def clean_education(education_list, connection):
    if education_list == None:
        return None, None
    elif len(education_list) == 5:
        school, program = education_list[0], education_list[-1]
        connection.execute('INSERT INTO link_rec_parsedprofile (school, school_program) VALUES (?, ?)', (school, program))
    elif len(education_list) == 1:  # this will mean school is only thing they put...
        school, program = education_list[0], None
        connection.execute('INSERT INTO link_rec_parsedprofile (school) VALUES (?)', (school))
    else:  # don't know when this will ever be used, len is almost always 1 or 5
        return None, None


def clean_experience(experience_list, connection):
    if experience_list == None:
        return None
    else:
        job_title_list = [experience_list[i] for i in range(len(experience_list)) if i % 2]
        company_list = [experience_list[i] for i in range(len(experience_list)) if i % 2 != 0]
        num = 0
        for i in range(len(job_title_list)):
            num += 1
            connection.execute('INSERT INTO link_rec_jobtitle (job%s) VALUES (?)' % (num), (job_title_list[i],))
            #connection.execute('INSERT INTO link_rec_jobtitle' + ' ' + ('job'+str(num)) + ' ' + 'VALUES (?)', (job_title_list[i]))
            #connection.execute('INSERT INTO link_rec_location' + ('loc'+str(num)) + 'VALUES (?)', (company_list[i]))

        #connection.execute('INSERT INTO link_rec_parsedprofile (school, school_program) VALUES (?, ?)', (school, program))
       # return job_title_list, company_list


def clean_header(header_list, connection):
    if len(header_list) == 3:
        name, title, url = header_list[0], header_list[1], header_list[-1]
        connection.execute('INSERT INTO link_rec_parsedprofile (name, header, url) VALUES (?, ?, ?)', (name, title, url))
    elif len(header_list) == 2:  # TODO: ASSUMPTION that title is missing...
        name, url = header_list[0], header_list[-1]
        connection.execute('INSERT INTO link_rec_parsedprofile (name, url) VALUES (?, ?)', (name, url))
    #else:
    #    return None, None, header_list[-1]  # really don't think it will ever reach this point


def parse_profiles_to_db(filename):
    conn = sqlite3.connect('/Users/Rahul/Desktop/Main/Side_projects/linkedin_recommend/db.sqlite3')
    c = conn.cursor()
    lines = open_file(filename)
    for url in lines[:3]:
        info_dict = linkedin.get_person_information(url)
        education_list = info_dict.get('education')
        experience_list = info_dict.get('experience')
        header_list = info_dict.get('header')
        clean_education(education_list, c)
        clean_experience(experience_list, c)
        clean_header(header_list, c)
    print('Done')
       # school, program = clean_education(education_list)
       # job_title_list, company_list = clean_experience(experience_list)
       # name, title, url = clean_header(header_list)
       # if school != None and program != None:
       #     pass
       # elif school != None and program == None:
       #     pass
       # else:
       #     pass
parse_profiles_to_db('linkedin_dest_url')



   # for url in lines:
   #     info_dict = linkedin.get_person_information(url)
   #     education_list = info_dict.get('education')
   #     if len(education_list) = 5:
   #         school, program = education_list[0], education_list[-1]
   #     elif len(education_list) = 1:
   #         school, program = education_list[0], None
   #     else:
   #         school, program = None, None  # TODO: Test it out first..
   #     experience_list = info_dict.get('experience')
   #     job_title_list = [experience_list[i] for i in range(len(experience_list)) if i % 2]
   #     company_list = [experience_list[i] for i in range(len(experience_list)) if i % 2 != 0]
   #     header_list = info_dict.get('header')
   #     name, title, url = header_list[0], header_list[1], header_list[-1]


    #c.execute('SELECT * FROM link_rec_profile')
    #c.execute('SELECT * FROM link_rec_parsedprofile')
    #y = c.fetchall()
    # c.execute("INSERT INTO app_file_feeds VALUES (?, ?, ?)", (recent_primary_key, title, link))
    # conn.commit()




#parse_profiles_to_db('linkedin_dest_url')



