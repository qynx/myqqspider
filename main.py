# from daos import  Crawler, Parser
from redis import Redis
from selenium import webdriver
from login import getCookie
from parse import parse, parse_one_log, get_content
import time
from utils.conns import connect_mysql, connect_redis
import configparser

class Runner():

    def __init__(self):
        self.browser = webdriver.Chrome()
        self.conf = configparser.ConfigParser()
        self.conf.read("my.ini", encoding="utf-8")
        
    def run(self):
        cookies = self.getCookie(self.browser, self.conf.get("qq", "account"),
        self.conf.get("qq", "password"))
        # wait for the dom to load
        
        time.sleep(3)
        # click the extend message button 
        expand_as = self.browser.find_elements_by_xpath('//a[@data-cmd="qz_toggle"]')
        for a in expand_as:
            a.click()
        time.sleep(3)
        self.parse(self.browser.page_source)        

def load_method(self):
    self.db_conn = connect_mysql()
    self.redis_client = connect_redis()
    self.getCookie = getCookie
    self.parse = parse
    self.parse_one_log = parse_one_log
    self.get_content = get_content

if __name__ == "__main__":
    load_method(Runner)
    runner = Runner()
    runner.run()