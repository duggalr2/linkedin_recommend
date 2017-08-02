import sqlite3
import nb_classification
import edu_classification

###################################################################################
# Automatically add classification to each new profile parsed or added by user!
###################################################################################


def update_profile(profile_url):
    """
    Update parsed profile with program and industry classification
    """
    conn = sqlite3.connect('/Users/Rahul/Desktop/Main/Side_projects/linkedin_recommend/db.sqlite3')
    c = conn.cursor()
    sql = "SELECT school_program FROM link_rec_allparsedprofile WHERE url= ?"
    c.execute(sql, (profile_url,))
    school_program = c.fetchone()
    sql = "SELECT id FROM link_rec_allparsedprofile WHERE url=?"
    c.execute(sql, (profile_url,))
    profile_id = c.fetchone()
    sql = "SELECT job FROM link_rec_alljobtitle WHERE profile_id=?"
    c.execute(sql, (profile_id[0],))
    job_list = c.fetchall()
    job_list_classification = nb_classification.predict_job(job_list)
    sql = "SELECT id FROM link_rec_alljobtitle WHERE profile_id=?"
    c.execute(sql, (profile_id[0],))
    job_id = c.fetchall()
    job_id = [y for i in job_id for y in i]
    for i in range(len(job_id)):
        sql = 'UPDATE link_rec_alljobtitle SET job_classification=? WHERE id=?'
        c.execute(sql, (job_list_classification[i], job_id[i]))
        conn.commit()
    print('Done!')

# TODO: Delete and combine with above...
def temp_edu_update(profile_url):
    conn = sqlite3.connect('/Users/Rahul/Desktop/Main/Side_projects/linkedin_recommend/db.sqlite3')
    c = conn.cursor()
    sql = "SELECT id, school_program FROM link_rec_allparsedprofile WHERE url= ?"
    c.execute(sql, (profile_url,))
    school_program = c.fetchone()
    if school_program[-1] is not None:
        prediction = edu_classification.predict_program(school_program[1:])
        sql = 'UPDATE link_rec_allparsedprofile SET program_classification=? WHERE id=?'
        i = prediction[0]
        c.execute(sql, (int(i), school_program[0]))
        conn.commit()
        # c.execute(sql, (prediction[0], school_program[0]))
        # conn.commit()
    else:
        pass

    # if prediction is not None:
    #     sql = "SELECT id FROM link_rec_allparsedprofile WHERE url=?"
    #     c.execute(sql, (profile_url,))
    #     profile_id = c.fetchone()
    #     sql = 'UPDATE link_rec_allparsedprofile SET program_classification=? WHERE id=?'
    #     c.execute(sql, (prediction[0], profile_id[0]))
    #     conn.commit()
    # print('Done!')

# temp_edu_update('https://www.linkedin.com/in/janhxie/')


def initial_update():
    conn = sqlite3.connect('/Users/Rahul/Desktop/Main/Side_projects/linkedin_recommend/db.sqlite3')
    c = conn.cursor()
    sql = 'SELECT url FROM link_rec_allparsedprofile WHERE id=?'
    # c.execute(sql, (68,))
    # print(update_profile(c.fetchone()[0]))
    for i in range(1, 215):
        sql = 'SELECT url FROM link_rec_allparsedprofile WHERE id=?'
        c.execute(sql, (i,))
        url = c.fetchone()
        temp_edu_update(url[0])
        # update_profile(url[0])

# initial_update()
# update_profile('https://www.linkedin.com/in/janhxie/')


def fix():
    conn = sqlite3.connect('/Users/Rahul/Desktop/Main/Side_projects/linkedin_recommend/db.sqlite3')
    c = conn.cursor()
    original_id = 107
    new_id = 108
    while True:
        if original_id == 207:
            break
        sql = 'UPDATE link_rec_alljobtitle SET profile_id=? WHERE profile_id=?'
        c.execute(sql, (new_id, original_id,))
        conn.commit()
        original_id += 1
        new_id += 1

# fix()



