#!/usr/bin/env python3
# coding: utf-8


from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.service import Service
from seleniumwire import webdriver as wire_driver

import base64
import numpy as np
import pandas as pd
import json
import os
import time
import logging

# Create log file: 

logging.basicConfig(filename="log.txt", level = logging.DEBUG, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Path of Chrome Driver and Config: 

driver_path       = os.getcwd()+ '\\Install_packages\\chromedriver.exe'
current_directory = os.getcwd()+ '\\config.json'     

#driver_path       = '.\\chromedriver.exe'
#current_directory =  '.\\config.json' 


# Import and Read Json Data File

with open(current_directory) as f:
    data = json.load(f)

print("Config File Loaded")

logging.info(driver_path)
logging.info(current_directory)

    
### Screen of Web Page with authentication

def screen_with_auth(url ,username , password):
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")
    
    s = Service(driver_path)
    
    driver = webdriver.Chrome(service=s, options=chrome_options)
    driver.get(url)
    driver.maximize_window()
    time.sleep(2)     

    # Create a list to get the position ( Login and Password ) and to be initialize after each iteration
    list_cred =[]
     
    links = driver.find_elements(By.XPATH,"//input[@type!='hidden']")
    

    for link in links: 
        list_cred.append(link.get_attribute('name'))       

    # LOGIN form   
           
    driver.find_element(By.XPATH, "//input[@name='" + list_cred[0] +"']").send_keys(username)
    driver.find_element(By.XPATH, "//input[@name='" + list_cred[1] +"']").send_keys(password)
    driver.find_elements(By.XPATH, "//button[@type='submit']")[0].click()    
    
    # Screening Part
    
    element= driver.find_element(By.XPATH,"//body") 
    width = 1920
    height = element.size['height'] + 1000
    driver.set_window_size(width,height)
    
    time.sleep(2)
    driver.save_screenshot('Webpage_Screen00.png')
    driver.quit()

    
### Screen of Web Page without authentication

def screen_without_auth(url ,username , password):
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")
    
    s = Service(driver_path)
    
    driver = webdriver.Chrome(service=s, options=chrome_options)
    driver.get(url)
    driver.maximize_window()
    time.sleep(2) 
 
    # Screening Part
    
    element= driver.find_element(By.XPATH,"//body") 
    width = 1920
    height = element.size['height'] + 1000
    driver.set_window_size(width,height)
    
    time.sleep(2)
    driver.save_screenshot('Webpage_Screen01.png')
    driver.quit()


### Screen of Web Page wit basic authentication


def screen_basic_auth (url ,username , password) :   
        
    Full_encoding = username +":" + password
    auth = (
    base64.encodebytes(Full_encoding.encode())
    .decode()
    .strip()
          )   
    
    def request_interceptorr(req):
        req.headers['Authorization'] = f'Basic {auth}'
        

    chrome_options= Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")

    s = Service(driver_path)

    chrome = wire_driver.Chrome(service=s, options=chrome_options)
    chrome.request_interceptor = request_interceptorr
    chrome.get(url)

    # Screening Part

    element= chrome.find_element(By.XPATH,"//body") 
    width = 1920
    height = element.size['height'] + 1000
    chrome.set_window_size(width,height)

    time.sleep(2)
    chrome.save_screenshot('Webpage_Screen02.png')
    chrome.quit()

    

# Change the Json file to DataFrame

df = pd.DataFrame(columns=["url","auth","user","pass","screenshotPath"])


for i in range(0,len(data)):
    currentItem = data[i]
    df.loc[i]   = [data[i]["url"],data[i]["auth"],data[i]["user"],data[i]["pass"],data[i]["screenshotPath"]]
    

# Screenshot_pages

for i in range(0,len(data)):
    
     if df.loc[i][1] == "none":
            
         screen_without_auth(df.loc[i][0],df.loc[i][2],df.loc[i][3])
         print(' Screen of the following URL :', df.loc[i][0] ,' generated successfully... ')
         logging.info(screen_without_auth)
     
     elif df.loc[i][1] == "form":
         screen_with_auth(df.loc[i][0],df.loc[i][2],df.loc[i][3])
         print(' Screen of the following URL :', df.loc[i][0] ,' generated successfully... ')
         logging.info(screen_with_auth)
     elif df.loc[i][1] == "basic":
         screen_basic_auth(df.loc[i][0],df.loc[i][2],df.loc[i][3])
         print(' Screen of the following URL :', df.loc[i][0] ,' generated successfully... ')
         logging.info(screen_basic_auth)
     else: 
        print("Done")



