from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
import pickle


class Scraper(object):

    def __init__(self, name, user, pw):
        self.browser = webdriver.Chrome(executable_path='D:/chromedriver')
        self.name = name.decode('utf-8')
        self.user = user
        self.pw = pw

    def log_in(self):
        url = 'https://www.instagram.com/accounts/login/'
        self.browser.get(url)
        self.browser.implicitly_wait(10)

        password = self.browser.find_element_by_name("password")
        username = self.browser.find_element_by_name("username")
        username.send_keys(self.user)
        password.send_keys(self.pw)

        self.browser.find_element_by_xpath("//button[contains(.,'Log in')]").click()

        try:
            self.browser.find_element_by_xpath("//button[contains(.,'Not Now')]").click()
        except NoSuchElementException:
            pass

        try:
            self.browser.find_element_by_xpath("//a[@href='/']").click()
        except NoSuchElementException:
            pass

    def search_user(self):
        search_bar = self.browser.find_element_by_xpath("//input[@placeholder='Search']")
        search_bar.send_keys(self.name)
        self.browser.implicitly_wait(5)
        self.browser.find_element_by_xpath("//a[@href='/" + self.name + "/']").click()
        self.browser.implicitly_wait(5)

    def find_photo_links(self):
        # edit for future work
        photos = self.browser.find_elements_by_xpath("//div[@class='v1Nh3 kIKUG  _bz0w']")

        links = []
        # get first 12 photos
        for photo in range(12):
            link = photos[photo].find_element_by_css_selector('a').get_attribute('href')
            links.append(link)

        return links

    def open_photo(self, link):
        # hardcoding char 25 onwards as quick hack - excluding 'https://www.instagram.com' at string beginning
        self.browser.implicitly_wait(10)
        self.browser.find_element_by_xpath("//a[@href='" + link[25:] + "']").click()
        self.browser.implicitly_wait(10)

        # catch no element exception for videos
        try:
            # edit for future work
            likes = self.browser.find_element_by_xpath("//a[@class='zV_Nj kCcVy']")
            photo_follower_n = int(likes.text.replace(' likes', '').replace(',', ''))
            likes.click()
            return photo_follower_n
        except NoSuchElementException:
            pass
            return 0

    def scroll_followers(self, n_followers):

        self.browser.implicitly_wait(10)
        dialog = self.browser.find_elements_by_xpath("//li[@class='NroHT']")
        tmp = 1
        while tmp < n_followers:
            self.browser.implicitly_wait(10)
            self.browser.execute_script("arguments[0].scrollIntoView();", dialog[tmp])
            tmp += 1
            if tmp != n_followers:
                dialog = self.check_more(tmp, dialog)

        print('no of likes: ' + str(len(dialog)))
        return dialog

    def check_more(self, counter, dialog):
        while counter == len(dialog):
            time.sleep((counter ** 0.5)/8)
            dialog = self.browser.find_elements_by_xpath("//li[@class='NroHT']")

        return dialog

    def get_follower_info(self, element):
        print('retrieving...')
        followers = [user.find_element_by_xpath("*//a[@title]").text for user in element]
        return followers

    def run(self):
        self.log_in()
        self.search_user()
        links = self.find_photo_links()

        all_followers = []
        counter = 1

        for link in links:
            print('extracting photo ' + str(counter) + ' of 12...' + ' for ' + self.name)
            n_followers = self.open_photo(link)

            if n_followers != 0:
                follower_elements = self.scroll_followers(n_followers)
                followers = self.get_follower_info(follower_elements)
                all_followers.extend(followers)
                all_followers = list(set(all_followers))

            # save data in the interim
            file_name = 'data/interm/followers_' + self.name + '_' + str(counter) + '.pickle'
            with open(file_name, 'wb') as file:
                pickle.dump(all_followers, file)

            self.browser.find_element_by_xpath("//button[contains(.,'Close')]").click()
            counter += 1

        return all_followers

    def close(self):
        self.browser.quit()




