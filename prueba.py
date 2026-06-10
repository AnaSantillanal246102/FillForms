import configparser
# import pandas as pd
import time
import os
import pandas as pd
import selenium.webdriver as webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import re
import random


def main():
    idRegex = r'id="(.*?)"'

    #setup the config parser (where the html identifiers are stored)
    config = configparser.ConfigParser()
    config.read('settings.ini')

    #setup the chrome webdriver
    driver = setupDriver()
    driver.get('https://secure7.saashr.com/ta/6206911.login?')

    #login to the website
    login(driver, config)
    waitToLoad(driver, By.XPATH, config.get('newcontractPath', 'nameI'))
    if driver.find_element(By.XPATH, config.get('contractsPath', 'menuB')):
        contracts(driver,config)
    waitToLoad(driver, By.XPATH, config.get('contractsPath', 'menuB'))
    haltStep()

    df = pd.read_excel(r'contracts.xlsx', sheet_name='Sheet1')

    #for ever row in the orders.xlsx file we will fill it out on the website
    for row in df.iterrows():

        #fill in the quantity and halt
        startInput = getIDs(driver, config, idRegex, True, pathHeading='newcontractPath', pathItem='startI')
        waitToLoad(driver, By.ID, startInput[0])
        driver.find_element(By.ID, startInput[0]).send_keys(row.get('Start'))
        haltStep()



    haltStep()

    driver.quit()

#setup the driver
def setupDriver():
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36 Edg/148.0.0.0'
    edge_driver_path = os.path.join(os.getcwd(), 'msedgedriver.exe')
    edge_service = Service(edge_driver_path)
    edge_options = Options()
    edge_options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Edge(service=edge_service, options=edge_options)
    driver.implicitly_wait(10)
    return driver

#logins the user to the website
def login(driver, config):
    driver.find_element(By.XPATH, config.get('loginPath', 'userName')).send_keys("asantillan@nadb.org")
    haltStep()  
    driver.find_element(By.XPATH, config.get('loginPath', 'password')).send_keys("227Santillan*")
    haltStep()
    driver.find_element(By.XPATH, config.get('loginPath', 'loginB')).click()
    haltStep()
    driver.implicitly_wait(20)

def contracts(driver,config):
    driver.find_element(By.XPATH, config.get('contractsPath', 'menuB')).click()
    haltStep()
    driver.find_element(By.XPATH, config.get('contractsPath', 'teamTab')).click()
    haltStep()
    driver.find_element(By.XPATH, config.get('contractsPath', 'hrB')).click()
    haltStep()
    driver.find_element(By.XPATH, config.get('contractsPath', 'maintenanceB')).click()
    haltStep()
    driver.find_element(By.XPATH, config.get('contractsPath', 'contractsB')).click()
    haltStep()
    driver.find_element(By.XPATH, config.get('contractsPath', 'addB')).click()
    haltStep()

def getIDs(driver, config, regexInput, searchClass, pathHeading=None, pathItem=None, element=None):
    innerHTML = ''
    if searchClass == True:
        #find the HTML code for the dynamic listbox (for selecting from the listbox)
        waitToLoad(driver, By.CLASS_NAME, config.get(pathHeading, pathItem))
        elements = driver.find_elements(By.CLASS_NAME, config.get(pathHeading, pathItem))
        innerHTML = elements[len(elements)-1].get_attribute('innerHTML')
    else:
        innerHTML = element.get_attribute('innerHTML')

    #find the id of the first element in the listbox and grab it
    ids = re.findall(regexInput, innerHTML)
    return ids

def waitToLoad(driver, byType, identifier):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((byType, identifier)))
    except:
        TimeoutException

#randomly stops the script between 1-3 seconds (to avoid detection)
def haltStep():
    int = random.randint(1, 5)
    time.sleep(int)

if __name__ == "__main__":
    main()