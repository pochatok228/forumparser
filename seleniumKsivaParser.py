from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class SeleniumKsivaParser:

    def __init__(self):
        self.driver = webdriver.Chrome('C:\\Users\\pochatok228\\Desktop\\forumparser\\chromedriver.exe')
        self.login = "madrigal.2014@mail.ru"
        self.password = '225354510'


    def openAndAuth(self):
        self.driver.get('https://3board.ksivi.bz/login/login')
        login_field = self.driver.find_element_by_name('login')
        login_field.send_keys(self.login)
        password_field = self.driver.find_element_by_name('password')
        password_field.send_keys(self.password)
        submit_button = self.driver.find_element_by_class_name('button--primary button button--icon button--icon--login')
        print(submit_button)
        submit_button.click()
        

if __name__ == '__main__':
    parser = SeleniumKsivaParser()
    parser.openAndAuth()