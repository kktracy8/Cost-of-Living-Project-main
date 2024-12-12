from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import re

zip = []

path = 'c:/Users/kykyk/OneDrive/Desktop/stations.csv'
file = open(path, 'w', encoding='utf-8')
file.write("state" + "," + "zip" +"," + "regular" +"," +"midgrade" +","+"premium"+","+"diesel"+"\n")

browser = webdriver.Firefox()
for x in zip:
    i = 1
    regular = 0
    midgrade = 0
    premium = 0
    diesel = 0
    while i < 5:
        baseURL = "http://www.gasbuddy.com/home?search=" + str(x) + "&fuel=" + str(i) +"&method=all"
        time.sleep(10)
        browser.get(baseURL)
        time.sleep(9)
        element = browser.find_element(By.XPATH, "/html/body").text
        a = re.findall("\d+\.\d+", element)
        fin = a[:-3]
        fl = [float(y) for y in fin]
        if i  == 1 and len(fl) != 0:
            regular = sum(fl)/len(fl)
        if i == 2 and len(fl) != 0:
            midgrade = sum(fl)/len(fl)
        if i == 3 and len(fl) != 0:
            premium = sum(fl)/len(fl)
        if i == 4 and len(fl) != 0:
            diesel = sum(fl)/len(fl)
        i += 1
    file.write("NV" + "," + str(x) +"," +str(regular) +"," +str(midgrade) +","+str(premium)+ "," + str(diesel) + "\n")

file.close()
browser.close()