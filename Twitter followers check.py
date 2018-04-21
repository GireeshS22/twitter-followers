# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 11:42:22 2018

@author: Gireesh Sundaram
"""
#%%

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

#%%
driver = webdriver.Chrome("C:/Users/Gireesh Sundaram/Downloads/chromedriver")
driver.get("https://www.twitter.com/login")

elem = driver.find_element_by_css_selector(".js-initial-focus")
elem.clear()
email = input("Enter your email or username here: ")
elem.send_keys(email)

elem = driver.find_element_by_css_selector(".js-password-field")
elem.clear()
password = input("Enter your password here: ")
elem.send_keys(password)

elem.send_keys(Keys.RETURN)
time.sleep(2)

#%%
elem = driver.find_element_by_partial_link_text("Followers")
elem.send_keys(Keys.RETURN)

#Scroll to end
for x in range(1, 10):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

#%%
pagesrc = driver.page_source
soup = BeautifulSoup(pagesrc, "lxml")

username = []
for users in soup.find_all("b", class_ = "u-linkComplex-target"):
    username.append(users.text)
    
userprofile = []
for users in soup.find_all("a", class_ = "fullname ProfileNameTruncated-link u-textInheritColor js-nav"):
    userprofile.append(users.text.strip())
    
#%%
#removing the first element of the list because if is your name and it is duplicate!
username.pop(0)
username.pop(0)

userprofile.pop(0)

#%%
#creatint a data frame together:
followers = pd.DataFrame(list(zip(userprofile, username)), columns = ["Profile", "Username"])
followers["username_upper"] = followers["Username"].str.upper()
followers = followers.sort_values(["username_upper"])
del followers["username_upper"]
followers.head()

#%%
#Saving the output to CSV file
followers.to_csv("Followers list.csv")
