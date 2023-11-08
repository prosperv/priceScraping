import sys
sys.path.insert(1, '../helper')
import siteHelper

import siteCarGurus as siteCarGurus


import seleniumFetcher
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from bs4 import BeautifulSoup

site = 'cargurus'

filter = {
    'maxPrice' : 35000,
    'minAutoYear' : 2016,
    'postalSearch' : 98087,
    'distance' : 100,
    'fuel' : "pluginhybrid",
    'make' : "toyota",
    'model' : "prius prime",
    'trim' : "advance",
}


browser = webdriver.Chrome()
browser.get("file:///home/pvan/priceScraping/priceListing/cargurus.html")

soup = BeautifulSoup(browser.page_source, 'html.parser')
mainTag = soup.find('main')
# elementMain:webdriver = browser.find_element(By.ID, "main")
# listOf = elementMain.find_elements(By.TAG_NAME, "script")

# cars = siteCarGurus.getCars()