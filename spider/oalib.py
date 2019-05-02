# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 00:31:03 2019

@author: Demonpw
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.support.wait import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.by import By
#import re

class search_by_oalib():
    
    def search(self,searchs):
        try:
            chrome_options=Options()
            #设置为无界面模式
            chrome_options.add_argument('--headless')
            browser = webdriver.Chrome(chrome_options=chrome_options)
            browser.implicitly_wait(10)
            browser.get("http://www.oalib.com")
            input = browser.find_element_by_name('kw')
            input.send_keys(searchs)
            input.send_keys(Keys.ENTER)
            temp=browser.find_element_by_xpath('//*[@id="form1"]/div/center/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div[3]/table/tbody/tr[1]/td/table/tbody/tr/td/span[1]/a')
            url=temp.get_attribute('href')
            title=browser.find_element_by_xpath('//*[@id="form1"]/div/center/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div[3]/table/tbody/tr[1]/td/table/tbody/tr/td/span[1]/a/u').text
            browser.get(url)
            temp=browser.find_element_by_link_text('Full-Text')
            pdf=temp.get_attribute('href')
            result={
                    'url':url,
                    'title':title,
                    #'citation':citation,
                    'pdf':pdf
                    }
            #wait=WebDriverWait(browser,10)
            #wait.until(EC.presence_of_element_located(By.XPATH,'//*[@id="buttons"]/ul/li[2]/a'))
            return result
        except:
            browser.close()