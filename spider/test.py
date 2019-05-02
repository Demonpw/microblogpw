# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 17:47:12 2019

@author: Demonpw
"""

from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import sys

    #chrome_options=Options()
    #设置为无界面模式
    #chrome_options.add_argument('--headless')
    #chrome_options=chrome_options
browser = webdriver.Chrome()
browser.implicitly_wait(10)
browser.get("https://item.jd.com/4113338.html")
pinglun=browser.find_element_by_xpath('//*[@id="detail"]/div[1]/ul/li[5]')
pinglun.click()
browser.execute_script("window.scrollTo(300,document.body.scrollHeight);")
browser.implicitly_wait(5)
sleep(2)

pinglungood=browser.find_element_by_xpath('//*[@id="comment"]/div[2]/div[2]/div[1]/ul/li[7]/a')
pinglungood.click()
#te=browser.find_element_by_class_name("comment-con");
#print(te.text)\
for i in range(11):
    if i != 0:
        te=browser.find_element_by_xpath('//*[@id="comment-6"]/div[{}]/div[2]/p'.format(i)).text+'\r\n'
        f= open ('1bad.txt','a',encoding='utf-8')
        f.write(te)
        f.close()
next_page=browser.find_element_by_link_text('下一页')
next_page.click()
sleep(2)
for j in range(33):
    sleep(1)
    page = browser.find_element_by_partial_link_text(u'下一页')
    browser.execute_script("arguments[0].scrollIntoView(false);", page)
    WebDriverWait(browser, 15).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, u'下一页'))).click()
    sleep(1)
    for i in range(11):
        if i != 0:
            te=browser.find_element_by_xpath('//*[@id="comment-6"]/div[{}]/div[2]/p'.format(i)).text+'\r\n'
            f= open ('1bad.txt','a',encoding='utf-8')
            f.write(te)
            f.close()
    sleep(7)
 #   def click_next(self,next_page,i):
 #       next_page=browser.find_element_by_class_name('shangpin|keycount|product|pinglunfanye-2')