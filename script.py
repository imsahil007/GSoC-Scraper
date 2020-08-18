URL = "https://summerofcode.withgoogle.com/organizations/"


from selenium import webdriver
from time import sleep

class GSocBot:

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get( URL )
        sleep(2)

GSocBot()