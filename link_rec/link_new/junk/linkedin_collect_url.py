import os, time, random, getpass, smtplib, sys, fileinput
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

########################################################################
#Linkedin Recommender Backend; Collects the names and urls!
#Only useful functions here are linkedin_login, linkedinrec_people, linkedin_main
    ##TODO: Figure out a way to safely save password so don't need to ask everytime;
########################################################################

chromedriver = '/Users/Rahul/Downloads/chromedriver'
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)
driver.set_window_size(1024, 768)
driver.maximize_window()

def linkedin_login():
    ''' Login's in to Linkedin '''
    driver.get('https://www.linkedin.com/')
    time.sleep(2)
    username = driver.find_element_by_id('login-email')
    password = driver.find_element_by_id('login-password')
    username.send_keys('duggalr42@gmail.com')
    try:
        pswd = getpass.getpass('Password: ')
        password.send_keys(pswd)
        password.submit()
        time.sleep(3)
        assert driver.current_url == 'https://www.linkedin.com/feed/'
    except:
        print('Error Signing in... ')

def linkedinrec_people(url):
    """ Get's the 10 "People Also Viewed" from a person's url """
    time.sleep(2)
    driver.get(url)
    driver.implicitly_wait(15)
    try:
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "right-rail")))
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "ul")))
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "li")))
        a = driver.find_element_by_class_name('right-rail')
        cr = driver.find_element_by_class_name('core-rail')
        yr = cr.find_element_by_tag_name('section')
        xr = yr.find_elements_by_tag_name('div')
        ar = xr[5].text.split('\n')
        sr = ar[0] + ' ' + ar[1]
        y = a.find_element_by_tag_name('ul')
        x = y.find_elements_by_tag_name('li')
        title = [x[i].text.replace('\n', ' ') for i in range(len(x))]
        title.append(sr)
        link = [i.find_element_by_tag_name('a').get_attribute('href') for i in x]
        link.append(url)
        profile_detail = driver.find_element_by_class_name('profile-detail')
        summary = profile_detail.find_elements_by_class_name('pv-entity__summary-info')
        # experience = [i.find_element_by_tag_name('h3').text for i in summary]
        # education = profile_detail.find_element_by_class_name('pv-entity__degree-info').text.split('\n')
        # accomplishment = profile_detail.find_element_by_class_name('pv-accomplishments-block__content')
        # print(accomplishment.text)
        # interest = profile_detail.find_element_by_class_name('pv-deferred-area__content')
        # int_li = interest.find_elements_by_tag_name('li')
        # for i in int_li:
        #     print(i.text)

        # return list(zip(title, link))
    except:
        print('Cannot find it..')
        driver.quit()

def linkedin_main(url):
    """
        Main Prompt, Has a starting profile link;
        Get's 10 "People Also Viewed" of 5 People in original recommendations of the start link;
    """
    start_link = url
    li = linkedinrec_people(start_link)

    # if len(li) == 0:
    #
    #     li = linkedinrec_people(start_link)

    if len(li) == 1:
        with open('linkedin_rec_people.txt', 'a') as f:
            for i in li:
                f.write(i[0])
                f.write(', ' + i[1])
                f.write('\n')
        return 'No "People Also Viewed" existed...'

    new_links = [i[1] for i in li]
    with open('linkedin_rec_people.txt', 'a') as f:
        for i in range(5):
            l = linkedinrec_people(new_links[i])
            for w in l:
                if w[0] not in open('linkedin_rec_people.txt').read():
                    f.write(w[0])
                    f.write(', ' + w[1])
                    f.write('\n')
    print('Done!')

def main():
    """
    Retrieve all url from file and send it to linkedin_main()
    """
    fs = open('linkedin_raw_url')
    lines= fs.readlines()
    lines = [line.replace('\n', '') for line in lines]
    for line in lines:
        linkedin_main(line)


if __name__ == '__main__':
    linkedin_login()
    print('Login Successful...')
    linkedinrec_people('https://www.linkedin.com/in/echeung94/')
    # url_1 = 'https://www.linkedin.com/in/ling-zhong-17ba9358/'
    # linkedin_main(url_1)
    # main()







################################################################################
                        # IGNORE ALL OF THIS!
################################################################################

def duplicate_checker(x): ##TODO: implement the files with hash table; especially as the list grows really large??
    with open('linkedin_rec_people.txt') as f, open('linkedin_data_collection.txt') as b:
        w = b.readlines()
        b = []
        for line in w: ##TODO: highly inefficient... is their a better way to compare without including last word???
            line = line.split()
            line = line[:-1]
            b.append(' '.join(line))
        for line in fileinput.input('linkedin_rec_people.txt', inplace=True):
            if x in w:
                line = line.replace(x, '')
            sys.stdout.write(line)
            fileinput.close()
            return True
        return False

def linkedin_prompt():
    with open('linkedin_rec_people.txt') as f:
        lines = f.readlines()
        while True:
            num = random.randrange(0, len(lines))
            x = lines[num]
            print('Checking if its a duplicate...')
            y = duplicate_checker(x)
            try:
                if not y:
                    x = x.replace('\n', '')
                    print(x)
                    s = input('Do you like this person (y/n): ')
                    if s == 'y':
                        ##TODO: send email and save name in separate 'data collection txt file';
                        with open('linkedin_data_collection.txt', 'a') as f:
                            f.write(x + ' yes')
                            f.write('\n')
                        server = smtplib.SMTP_SSL('smtp.googlemail.com', 465)
                        gmail_user = 'duggalr42@gmail.com'
                        password = 'Umakant12'
                        to_email = 'ibrahul24@gmail.com'
                        body = 'hey, there how are you!'
                        server.login(gmail_user, password)
                        server.sendmail(gmail_user, to_email, body)
                        print('Email Sent..')
                        driver.quit()
                        break
                elif y:
                    continue

            except:
                with open('linkedin_data_collection.txt', 'a') as f:
                    f.write(x + ' no')
                    f.write('\n')

def linkedin_search():
    linkedin_login()
    time.sleep(2)
    x = driver.find_element_by_class_name('type-ahead-input')
    search = x.find_element_by_tag_name('input')
    search.send_keys('harvard')
    search.send_keys(Keys.ENTER)
    time.sleep(8)
    new_url = (driver.current_url).replace('index', 'schools')
    new_url = new_url.replace('GLOBAL_SEARCH_HEADER', 'SWITCH_SEARCH_VERTICAL')
    driver.get(new_url)
    time.sleep(5)
    driver.find_element_by_css_selector('#ember1790').click()
    time.sleep(5)
    x = driver.find_element_by_class_name('company-actions-bar')
    x.find_element_by_tag_name('a').click()
    time.sleep(5)
    start_year = driver.find_element_by_id('alumni-search-year-start')
    end_year = driver.find_element_by_id('alumni-search-year-end')
    start_year.send_keys('2014')
    start_year.send_keys(Keys.ENTER)
    time.sleep(3)
    list_of_people = driver.find_elements_by_class_name('org-alumni-profiles-module__profiles-list-item')
    for i in list_of_people:
        print(i.text)
