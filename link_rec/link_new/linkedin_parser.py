import os, time, getpass
from timeit import default_timer as timer
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

############################################################################################
        # Linkedin Basic Parser: Parse's profile header, experience and education
############################################################################################


class Linkedin(object):

    """ Linkedin Parser using Selenium """

    def __init__(self):
        """
        Initialize Chromedriver
        """
        self.count = 0 # for error purposes..
        chromedriver = '/Users/Rahul/Downloads/chromedriver'
        os.environ["webdriver.chrome.driver"] = chromedriver
        self.driver = webdriver.Chrome(chromedriver)
        self.driver.set_window_size(1024, 768)
        self.driver.maximize_window()

    def linkedin_login(self):
        """
        Login's in to Linkedin; Password input using getpass
        """
        self.driver.get('https://www.linkedin.com/')
        time.sleep(1)
        username = self.driver.find_element_by_id('login-email')
        password = self.driver.find_element_by_id('login-password')
        username.send_keys('duggalr42@gmail.com')
        try:
            pswd = getpass.getpass('Password: ')  # not the most ideal but safest way for now...
            password.send_keys(pswd)
            password.submit()
            time.sleep(1)
            assert self.driver.current_url == 'https://www.linkedin.com/feed/'
        except:
            raise Exception('Error Logging in...')

    def get_person_header(self, url):
        """
        Return the Person's Name + Header + Url
        """
        self.driver.get(url)
        ret_list = []
        try:
            wait = WebDriverWait(self.driver, 20)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "pv-top-card-section__body")))

            try:
                initial_div = self.driver.find_element_by_class_name('pv-top-card-section__body')
                main_div = initial_div.find_element_by_tag_name('div')
                name = main_div.find_element_by_tag_name('h1')
                ret_list.append(name.text)
                header = main_div.find_element_by_tag_name('h2')
                ret_list.append(header.text)
                ret_list.append(url)
            except:
                pass

            return ret_list

        except:
            raise Exception('Cannot find it..')

    def get_people_viewed(self, url):
        """
        Parses's the Person's Name + Header and also parse's the 10 "People Also Viewed" from a person's url
        Returns list of tuples with (Name + Header, url)
        If people also viewed option not available, list will just be len(1)
        (Rarely, Selenium doesn't pick up the JS DOM, so the script tries 2 more times before raising an exception)
        """
        self.driver.get(url)
        # count = 0
        try:
            wait = WebDriverWait(self.driver, 20)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "right-rail")))
            # wait.until(EC.presence_of_element_located((By.TAG_NAME, "ul")))
            # wait.until(EC.presence_of_element_located((By.TAG_NAME, "li")))
            a = self.driver.find_element_by_class_name('right-rail')
            cr = self.driver.find_element_by_class_name('core-rail')
            y = a.find_element_by_tag_name('ul')
            x = y.find_elements_by_tag_name('li')
            link = [i.find_element_by_tag_name('a').get_attribute('href') for i in x]
            link.append(url)
            return link
        except:
            raise Exception('Tried and Cannot find it..')
            # self.driver.quit()

    def __get_person_experience(self, section, url):
        """
        A private helper function to get_person_info(): Return's list of profile experience section
        Parameter: -section: experience section selenium element
                   -url: url of profile
        """
        try:
            exp_ul = section.find_element_by_tag_name('ul')
            # exp_li = exp_ul.find_elements_by_tag_name('li')
            tt = exp_ul.find_elements_by_class_name('pv-entity__summary-info')

            if len(tt) >= 1:
                experience_list = []
                for i in tt:
                    # tt = i.find_element_by_class_name('pv-entity__summary-info')
                    title = i.find_element_by_tag_name('h3').text
                    co = i.find_element_by_tag_name('h4')
                    l = i.find_elements_by_tag_name('span')
                    company_name = l[1].text
                    experience_list.append(title)
                    experience_list.append(company_name)
                return experience_list
        except:
            print("Probably JS didn't render probably (try loading script again) "
                  ", there is no experience section on the profile!")
            print("Profile link", url)

    def __get_person_education(self, section, url):
        """
        A private helper function to get_person_info(): Return's list of profile education section (error message otherwise)
        Parameter: -section: education section selenium element
                   -url: url of profile
        """
        education_ul = section.find_element_by_tag_name('ul')
        education_li = education_ul.find_element_by_tag_name('li')
        edu_list = []
        try:
            education_info = education_li.find_element_by_class_name('pv-entity__degree-info')
            edu_list.append(education_info.text.split('\n'))

        except:
            print("Probably JS didn't render probably (try loading script again) "
                  "or there is no education section on the profile!")
            print("Profile link", url)

        edu_list = [y for i in edu_list for y in i]
        return edu_list

    def get_person_information(self, url):
        """
        Return's summary of an individual person in the form of a dict: includes education, header, experience
        (Only the most recent experience is included, doesn't included 'see more positions')
        """
        self.driver.get(url)
        # self.driver.get(url)
        # self.driver.implicitly_wait(15)
        main_dictionary = {}
        try:
            wait = WebDriverWait(self.driver, 15)
            # wait.until(EC.presence_of_element_located((By.CLASS_NAME, "profile-detail")))
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "background-details")))
            span = self.driver.find_element_by_class_name('background-details')
            main_section = span.find_element_by_tag_name('section') # should be present on everyone's profile
            all_section = main_section.find_elements_by_tag_name('section')

            if len(all_section) >= 2:
                id_first = all_section[0].get_attribute('class')
                if 'education-section' not in id_first:
                    experience_section = all_section[0]
                    experience_list = self.__get_person_experience(experience_section, url)
                    main_dictionary['experience'] = experience_list

                # Assuming that the second section attribute will be education...
                # Double checking... shouldn't raise assertion error though
                education_section = all_section[1]
                id_second = education_section.get_attribute('class')
                assert 'education-section' in id_second
                education_list = self.__get_person_education(education_section, url)
                main_dictionary['education'] = education_list

            if len(all_section) == 1:
                id_first = all_section[0].get_attribute('class')
                if 'education-section' not in id_first:
                    experience_section = all_section[0]
                    experience_list = self.__get_person_experience(experience_section, url)
                    main_dictionary['experience'] = experience_list
                    main_dictionary['education'] = []

                else: # it is education
                    education_section = all_section[0]
                    id_second = education_section.get_attribute('class')
                    assert 'education-section' in id_second
                    education_list = self.__get_person_education(education_section, url)
                    main_dictionary['education'] = education_list
                    main_dictionary['experience'] = []

            if len(all_section) == 0:
                # nothing there...
                main_dictionary['education'] = []
                main_dictionary['experience'] = []
                print("Didn't find experience or education on the profile..")
                print("Double Check the profile", url)

            header = self.get_person_header(url) # list of basic info: name, header, url
            main_dictionary['header'] = header
            return main_dictionary

        except:
            if self.count == 2:
                raise Exception(
                    'Tried 2 times, Reload the Script, this is probably the internet or JS taking too long...')
            self.count += 1
            self.get_person_information(url)

# First time, uncomment and run everything below, if all passed, everything is good;
# if __name__ == '__main__':
#     x = Linkedin()
#     x.linkedin_login()
#     print(x.get_person_information('https://www.linkedin.com/in/hollyx/'))
#     x.get_person_information('https://www.linkedin.com/in/imanjaffari/')
#     x.get_person_information('https://www.linkedin.com/in/melissaleighjohnson/')
#     x.get_person_information('https://www.linkedin.com/in/jiahui-jiang-569a0a39/')
#     x.get_person_information('https://www.linkedin.com/in/rahul-duggal-402506134/')
#     x.get_person_information('https://www.linkedin.com/in/jessica-chee/')
#     x.get_person_information('https://www.linkedin.com/in/sharmaabhinav/')
#     x.get_people_viewed('https://www.linkedin.com/in/jessica-chee/')
#     x.get_people_viewed('https://www.linkedin.com/in/rahul-duggal-402506134/')
#     x.get_person_header('https://www.linkedin.com/in/sharmaabhinav/')
#     x.get_person_header('https://www.linkedin.com/in/ling-zhong-17ba9358/')
#     x.get_person_header('https://www.linkedin.com/in/rahul-duggal-402506134/')
