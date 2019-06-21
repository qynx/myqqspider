# version: python3.7
# for login method
from logger import logger as logging
import requests
import time
import json
import random
import umsgpack

def getCookie(self, browser, account, password, dama=False):
    """ 根据QQ号和密码获取cookie """
    failure = 0
    while failure < 2:
        try:
            browser.get('http://qzone.qq.com/')

            try:
                access = browser.find_element_by_id('guideSkip')  # 继续访问触屏版按钮
                access.click()
                time.sleep(1)
            except Exception as e:
                pass
            login_frame = browser.find_element_by_xpath("//iframe[@id='login_frame']")
            browser.switch_to_frame(login_frame)
            login_a = browser.find_element_by_xpath("//a[@id='switcher_plogin']")
            login_a.click()
            account_input = browser.find_element_by_id('u')  # 账号输入框
            password_input = browser.find_element_by_id('p')  # 密码输入框
            go = browser.find_element_by_id('login_button')  # 登录按钮
            account_input.clear()
            password_input.clear()
            account_input.send_keys(account)
            password_input.send_keys(password)
            go.click()

            try:
                # 如果可以成功找到元素 界面还有登录框 则登录失败
                login_frame = browser.find_element_by_xpath("//iframe[@id='login_frame']")
                raise Exception("账号或密码错误")
            except Exception:
                logging.debug("login successfully")
              
            cookies = self.browser.get_cookies()
            self.redis_client.set(str(account)+"_cookie", umsgpack.packb(cookies))
            logging.info("get cookie successfully")
            return
        except Exception as e:
            logging.exception(e)
            failure = failure + 1
            if 'browser' in dir():
                browser.quit()
        except KeyboardInterrupt as e:
            raise e
    return ''
