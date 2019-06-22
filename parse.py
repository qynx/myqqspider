from lxml.html import fromstring
from logger import logger as logging
from lxml import etree
from utils.talks import Talk
import re
import time


def get_content(self, li):
        '''
        get the content of one log
        need to judge where the log is complete
        @param li: lxml li dom
        @return type str: html code of log content
        '''
        complete_div = li.xpath('.//div[@class="f-info qz_info_complete"]')
        if len(complete_div) > 0:
                div = complete_div[0]
        else:
                div = li.xpath('.//div[@class="f-info"]')[0]
        return etree.tostring(div, encoding="utf-8", method="html").decode("utf-8")

def parse_one_log(self, li):
    '''
    extract info from one log
    @param li: lxml dom node
    @return one Log object
    '''
    logging.info("start parse one log")
    li_id = li.xpath(".//@id")[0]
    time_string = re.findall("\w+_\d+_\d+_\d+_(\d+)_\d_\d", li_id)[0]
    pub_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time_string)))
    name = li.xpath(".//div[@class='user-info']//a//text()")[0]
    img_src = li.xpath(".//div[@class='user-pto']//img//@src")[0]
    user_href = li.xpath(".//div[@class='user-pto']//a//@href")[0]
    info_html = self.get_content(li)
    # 
    images = li.xpath(".//a[@class='img-item  ']//img//@src")
    big_images = li.xpath(".//a[@class='img-item  ']//@href")
    # import pdb; pdb.set_trace()
    
    # make up
    talk = Talk()
    talk.name = name
    talk.author = user_href
    talk.content = info_html
    talk.images = images
    talk.time = pub_time
    talk.li_id = li_id
    talk.big_images = big_images                                   
    talk.insert(self.db_conn.cursor())
    self.db_conn.commit()
    # #


def parse_ul(self, ul):
    '''
    parse lxml ul dom contains a list of log
    '''
    lis = ul.xpath(".//li[@class='f-single f-s-s']") 
    for li in lis:
        self.parse_one_log(li)

def parse(self, html):
    logging.info("start find and parse log list")
    doc = fromstring(html)
    ul = doc.xpath("//ul[@id='feed_friend_list']")[0]
    # choose by class to remove ad
    lis = ul.xpath(".//li[@class='f-single f-s-s']") 
    for li in lis:
        self.parse_one_log(li)
    self.page_down()
    ul = self.get_new_ul()
    self.parse_ul(ul)

def page_down(self):
    ''' 
    page down to get old log
    '''
    js = "var q=document.documentElement.scrollTop=100000"  
    self.browser.execute_script(js)
    # wait for data to load
    time.sleep(3)
    expand_as = self.browser.find_elements_by_xpath('//a[@data-cmd="qz_toggle"]')  
    for a in expand_as:
        a.click()
    time.sleep(3)
    self.EXTRA_CURR_PAGE += 1

def get_new_ul(self):
    '''
    after page down get the ul
    '''
    curr_page_source = self.browser.page_source
    root = fromstring(curr_page_source)
    ul = root.xpath('//ul[@data-page="%s"]' % self.EXTRA_CURR_PAGE)[0]
    return ul
