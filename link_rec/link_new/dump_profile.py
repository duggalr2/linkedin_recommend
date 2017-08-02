import linkedin_parser
import sqlite3
import time

####
# Personal Linkedin Function to fill up database with profiles....
####


def open_file(filename):
    f = open(filename)
    lines = f.readlines()
    return [line.replace('\n', '') for line in lines if len(line)>1]


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


def get_education_data(items):
    """
    Return's list of all the university name's and degree name
    """
    try:
        university_name = None
        degree = None
        education = items.get('education')
        if 'Field Of Study' in education:
            y = education.index('Field Of Study')
            degree = education[y + 1]
        uni_name = education[0]
        return uni_name, degree
    except:
        return None, None


def clean_education(profile_id, university, university_name, header_list, connection, conn):

    if university is not None and university_name is not None:
        if header_list[1] is not None:
            name, title, url = header_list[0], header_list[1], header_list[-1]
            connection.execute(
                'INSERT INTO link_rec_allparsedprofile (id, name, header, url, school, school_program) VALUES (?, ?, ?, ?, ?, ?)',
                (profile_id, name, title, url, university, university_name,))
            conn.commit()

        elif header_list[1] is None:
            name, url = header_list[0],  header_list[-1]
            connection.execute('INSERT INTO link_rec_allparsedprofile (id, name,  url, school, school_program) VALUES (?, ?, ?, ?, ?)', (profile_id, name, url, university, university_name,))
            conn.commit()

    elif university_name is None:
        if header_list[1] is not None:
            name, title, url = header_list[0], header_list[1], header_list[-1]
            connection.execute(
                'INSERT INTO link_rec_allparsedprofile (id, name, header, url, school) VALUES (?, ?, ?, ?, ?)',
                (profile_id, name, title, url, university,))
            conn.commit()

        elif header_list[1] is None:
            name, url = header_list[0],  header_list[-1]
            connection.execute('INSERT INTO link_rec_allparsedprofile (id, name, url, school) VALUES (?, ?, ?, ?)', (profile_id, name, url, university,))
            conn.commit()

    else:
        return None


def clean_experience(profile_id, experience_list, header_list, connection, conn):

    if experience_list is None:
        return None

    else:
        company_name = [experience_list[i] for i in range(len(experience_list)) if i%2]
        job_title = [experience_list[i] for i in range(len(experience_list)) if i%2 == 0]
        assert len(company_name) == len(job_title)
        conn = sqlite3.connect('/Users/Rahul/Desktop/Main/Side_projects/linkedin_recommend/db.sqlite3')
        c = conn.cursor()
        # c.execute('SELECT id FROM link_rec_allparsedprofile ORDER BY id DESC LIMIT 1')
        c.execute('SELECT id FROM link_rec_alljobtitle ORDER BY id DESC LIMIT 1')
        original_id = c.fetchone()
        new_id = 0
        if original_id is not None:
            new_id = original_id[0] + 1

        for i in range(len(company_name)):
            connection.execute('INSERT INTO link_rec_alllocation (id, profile_id, loc) VALUES (?, ?, ?)', (new_id, profile_id, company_name[i],))
            conn.commit()
            connection.execute('INSERT INTO link_rec_alljobtitle (id, profile_id, job) VALUES (?, ?, ?)', (new_id, profile_id, job_title[i],))
            conn.commit()
            new_id += 1


def clean_header(header_list):

    if len(header_list) == 3:
        name, title, url = header_list[0], header_list[1], header_list[-1]
        return name, title, url

    elif len(header_list) == 2:  # TODO: ASSUMPTION that title is missing...
        name, title, url = header_list[0], None,  header_list[-1]
        return name, title, url


def parse_profiles_to_db(filename, start_iter=0, end_iter=100, interval=7):
    # THE LENGTH OF THE FILE NEEDS TO BE BIGGER THAN 7!

    conn = sqlite3.connect('/Users/Rahul/Desktop/Main/Side_projects/linkedin_recommend/db.sqlite3')
    c = conn.cursor()
    lines = open_file(filename)  # url file
    c.execute('SELECT id FROM link_rec_allparsedprofile ORDER BY id DESC LIMIT 1')
    original_id = c.fetchone()
    new_id = 0
    num = 0
    length_lines = len(lines)

    if original_id is not None:
        new_id = original_id[0] + 1

    while interval <= end_iter:

        if num == 7:
            time.sleep(40)
            num = 0
            start_iter += 7
            interval += 7

        for url in lines[start_iter:interval]:
            info_dict = linkedin.get_person_information(url)

            if info_dict is not None:
                university_name, university_program = get_education_data(info_dict)
                experience_list = info_dict.get('experience')
                header_list = info_dict.get('header')
                new_header_list = clean_header(header_list)
                clean_education(new_id, university_name, university_program, new_header_list, c, conn)
                clean_experience(new_id, experience_list, header_list, c, conn)
                new_id += 1
                conn.commit()

            else:
                continue

            num += 1

    user_input = input('Should I delete the urls in link_dest_url (y/n): ')
    if user_input == 'y':
        with open('linkedin_dest_url', 'w'):
            pass
    else:
        pass

    print('Done!')


if __name__ == '__main__':
    linkedin = linkedin_parser.Linkedin()
    linkedin.linkedin_login()
    # dump_profiles(2)
    parse_profiles_to_db('linkedin_dest_url', 80, 140)

    # conn = sqlite3.connect('/Users/Rahul/Desktop/Main/Side_projects/linkedin_recommend/db.sqlite3')
    # c = conn.cursor()
    # lines = open_file('linkedin_dest_url')
    # id = 864
    # num = 0
    #
    # for url in lines:
    #     info_dict = linkedin.get_person_information(url)
    #
    #     if info_dict is not None:
    #         university_name, university_program = get_education_data(info_dict)
    #         experience_list = info_dict.get('experience')
    #         header_list = info_dict.get('header')
    #         new_header_list = clean_header(header_list)
    #         clean_education(university_name, university_program, new_header_list, c, conn)
    #         clean_experience(id, experience_list, header_list, c, conn)
    #         id += 1
    #         conn.commit()
    #
    #     else:
    #         continue
