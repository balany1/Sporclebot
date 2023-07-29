from numpy import append
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common import keys
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import os
from os.path import expanduser
from pathlib import Path
from airflow.models import DAG
from datetime import datetime
from datetime import timedelta



class SporcleAutobot():

    def __init__(self, headless: bool = False):

        if headless:
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--start-maximized")
            chrome_options.headless = True
            self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        else:
            self.driver = webdriver.Chrome(ChromeDriverManager().install())

    
    def load_page(self):
        '''Opens the Meatloaf page'''
        self.driver.get("https://www.sporcle.com/games/armeenrashid/what-is-the-only-thing-a-meatloaf-wont-do-for-love")
        time.sleep(3)

    def login(self):
        '''logs user in if not already done so'''
        try:
            sign_in_button = self.driver.find_element(by=By.XPATH, value="//*[@id='user-not-logged-in']")
            sign_in_button.click()
        except NoSuchElementException:
            pass
        
        time.sleep(3)
        self.driver.find_element(by=By.XPATH, value="/html/body/div[12]/div/div/div/div[3]")
        email_address = self.driver.find_element(by=By.XPATH, value="//*[@id='email']")
        email_address.send_keys("andrewmcnamara@live.co.uk")
        password = self.driver.find_element(by=By.XPATH, value="//*[@id='password']")
        password.send_keys("T00narmyspc")
        login_button = self.driver.find_element(by=By.XPATH, value="//*[@id='log-in-button']")
        login_button.click()
    

    def accept_cookies(self):
        '''Switches to cookies frame and clicks the accept button'''
        accept_cookies_frame = self.driver.switch_to.frame(self.driver.find_element(by= By.XPATH, value = "//*[@id='sp_message_iframe_756623']"))
        accept_cookies = self.driver.find_element(by=By.XPATH, value="//*[@id='notice']/div[5]/button[2]")
        accept_cookies.click()

    def play_game(self):
        
        time.sleep(3)
        play_button = self.driver.find_element(by=By.XPATH, value="//*[@id='button-play']")
        play_button.click()
        time.sleep(3)


    def find_answer(self):
        '''Clicks the button(s) required to finish the quiz'''
        time.sleep(3)
        answer_button = self.driver.find_element(by=By.XPATH, value = "//*[@id='slot0']/div")
        answer_button.click()
        time.sleep(2)

if __name__ == "__main__":
    bot = SporcleAutobot(headless= True)
    bot.load_page()
    bot.accept_cookies()
    bot.login()
    bot.play_game()
    bot.find_answer()
    bot.driver.quit()
    
