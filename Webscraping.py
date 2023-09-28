#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 18:27:45 2023

@author: glenn
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import pandas as pd


url = "https://infrastructurepipeline.org/search"

option = webdriver.ChromeOptions()

#Removes navigator.webdriver flag
option.add_argument('--disable-blink-features=AutomationControlled')


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                         options=option)
driver.get(url)

time.sleep(3)

driver.find_element(By.XPATH,"/html/body/div/main/div[3]/div[2]/div[1]/div[2]/button[2]").click()

time.sleep(3)

previous_height= driver.execute_script('return document.body.scrollHeight')

while True:
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    
    time.sleep(5)
    
    new_height = driver.execute_script('return document.body.scrollHeight')
    
    if new_height == previous_height:
        break
    previous_height = new_height


        
soup = BeautifulSoup(driver.page_source, "html.parser")

df = pd.DataFrame(columns=["Project Names"])
results = soup.find_all("div", class_="project-name")

for i in range(len(results)):
    # print(results[i].text)
    df.loc[i + 1] = [results[i].text]
    
df.to_csv("test.csv")
