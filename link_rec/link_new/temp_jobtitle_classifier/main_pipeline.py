import sqlite3
import nb_classification
import edu_classification
import pandas as pd
import regex

job_path = '/Users/Rahul/Desktop/Main/Side_projects/linkedin_recommend/link_rec/link_new/temp_jobtitle_classifier/job_classified'
edu_path = '/Users/Rahul/Desktop/Main/Side_projects/linkedin_recommend/link_rec/link_new/temp_jobtitle_classifier/edu_classified'
job_title = pd.read_table(job_path, header=None, sep='=>', names=['title', 'label'])
# job_title['label_num'] = job_title.label({'software':0, 'engineering':1, 'research':2, 'design':3, 'data_science':4,
#                                           'product_manager':5, 'business_finance':6, 'startup_founder':7,
#                                           'admin_it':8, 'crypto':9})

# print(job_title)

X = job_title.title
Y = job_title.label


def update_profile(profile_id):
    """Updates both Job and Education Classificaiton given the profile_id"""
    conn = sqlite3.connect('/Users/Rahul/Desktop/Main/Side_projects/linkedin_recommend/db.sqlite3')
    c = conn.cursor()
    sql = "SELECT job FROM link_rec_alljobtitle WHERE profile_id=?"
    c.execute(sql, (profile_id,))
    job_list = c.fetchall()
    sql = "SELECT school_program FROM link_rec_allparsedprofile WHERE id=?"
    c.execute(sql, (profile_id,))
    program = c.fetchone()

    if program[0] is not None:
        prediction = edu_classification.predict_program(program[0:], X, Y)
        sql = 'UPDATE link_rec_allparsedprofile SET program_classification=? WHERE id=?'
        i = prediction[0]
        c.execute(sql, (int(i), profile_id))
        conn.commit()
        with open(edu_path, 'a') as f:
            edu_list = [regex.tokenize_and_stem(program[0])]
            edu_list = [' '.join(job) for job in edu_list]
            f.write(edu_list[0] + ', ' + i + '\n')

    if len(job_list) > 0:
        job_list_classification = nb_classification.predict_job(job_list)
        sql = "SELECT id FROM link_rec_alljobtitle WHERE profile_id=?"
        c.execute(sql, (profile_id,))
        job_id = c.fetchall()
        job_id = [y for i in job_id for y in i]
        for i in range(len(job_id)):
            sql = 'UPDATE link_rec_alljobtitle SET job_classification=? WHERE id=?'
            c.execute(sql, (job_list_classification[i], job_id[i]))
            conn.commit()
        with open(job_path, 'a') as f:
            job_list = [job for j in job_list for job in j]
            new_job_list = [regex.tokenize_and_stem(i) for i in job_list]
            new_job_list = [' '.join(job) for job in new_job_list]
            for i in range(len(new_job_list)):
                job = ''.join(new_job_list[i])
                f.write(job + '=>' + str(job_list_classification[i]) + '\n')

    # print('Done!')


# if __name__ == '__main__':
#
#     conn = sqlite3.connect('/Users/Rahul/Desktop/Main/Side_projects/linkedin_recommend/db.sqlite3')
#     c = conn.cursor()
#     sql = 'SELECT id FROM link_rec_allparsedprofile WHERE url=?'
#     url = 'https://www.linkedin.com/in/john-yeung-139b244b/'  # This is what you need to update each time!
#     c.execute(sql, (url,))
#     profile_id = c.fetchone()
#     sql = 'SELECT id FROM link_rec_allparsedprofile ORDER BY id DESC LIMIT 1'
#     c.execute(sql)
#     last_id = c.fetchone()
#
#     for i in range(profile_id[0], last_id[0]+1):
#         update_profile(i)
