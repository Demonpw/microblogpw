# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 13:10:13 2019

@author: Demonpw
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.support.wait import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.by import By
import re
import sys
class search_by_scihub():
    
    def search(self,searchs):
        try:
            searchs=sys.argv[1]
            chrome_options=Options()
            #设置为无界面模式
            chrome_options.add_argument('--headless')
            browser = webdriver.Chrome(chrome_options=chrome_options)
            browser.implicitly_wait(10)
            browser.get("http://www.sci-hub.tw")
            input = browser.find_element_by_name('request')
            input.send_keys(searchs)
            input.send_keys(Keys.ENTER)
            url=browser.current_url
            title=browser.title
            #citation=browser.find_element_by_id('citation').text
            #browser.switch_to.frame('pdf')
            temp=browser.find_element_by_xpath('//*[@id="buttons"]/ul/li[2]/a')
            if temp is None:
                title='None'
                url='None'
                pdf='None'
            else: 
                pdf=temp.get_attribute('onclick')
                #location.href='//sci-hub.tw/downloads/2019-01-28//61/silver2017.pdf?download=true'
                regex_str=".*?//(.*)\?download=true\'"
                pdf=re.match(regex_str,pdf).group(1)
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
            print(e)
            result={
                    'url':'None',
                    'title':'None',
                    #'citation':citation,
                    'pdf':'None'
                    }
            return result