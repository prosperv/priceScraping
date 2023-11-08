import sys
sys.path.insert(1, '../helper')

import json
from bs4 import BeautifulSoup
import re
from nameParser import *
import seleniumFetcher
import simpleFetcher
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import urllib.parse


# "items": [
# [
#     15124445, //Distance? 0
#     2148355, // 1
#     145, // Vehicle 2
#     5900, // Price 3
#     "1:1~46.7998~-122.8214", //gps 4
#     [
#     4, // Photo 5
#     "3:00M0M_eaguGvdEOak_0oo0ww",
#     ],
#     [
#     6,
#     "bucoda-2014-chevy-volt-plug-in-hybrid" // url name 6
#     ],
#     [
#     9,
#     248000 // Milage 7
#     ],
#     "2014 Chevy Volt Plug-in Hybrid - High Mileage, Leather Seats, Bose Rad"
# ],

def searchUrl(subString, urlList):
    foundUrl = ""
    for url in urlList:
        if url.find(str(subString)) >= 0:
            foundUrl = url
            break

    if (len(foundUrl) > 0):
        urlList.remove(foundUrl)
    return foundUrl


def parse(soup, urlList):
    clVehicleId = 145
    database = []
    jsonString = soup.text
    data = json.loads(jsonString)['data']
    listings = data['items']

    for thing in listings:
        # Filter because craigslist is wierd
        if thing[2] == clVehicleId:
            url = searchUrl(thing[6][1], urlList)
            if len(url) > 0:
                c = {
                    "make": findMakerName(thing[9]),  # parse
                    "model": findModelName(thing[9]),  # parse
                    "trim": "",
                    "year": findYear(thing[9], 2010),
                    "price": thing[3],
                    "milage": thing[7][1],
                    "shippingcost": 0,
                    "distance": None,
                    "city": thing[6][1].split()[0],  # parse
                    "state": "WA",
                    "vin": "seeSite",
                    "link": url,
                    "webhost": "craigslist",
                }
                print(c)
                database.append(c)
        else:
            print(".")
    return database


urlJson = "https://sapi.craigslist.org/web/v8/postings/search/full?batch=2-0-360-0-0&cc=US&excats=5-2-13-22-2-24-1-4-19-1-1-1-1-1-1-3-6-10-1-1-1-2-2-8-1-1-1-1-1-4-1-7-1-1-1-1-7-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-2-1&lang=en&max_price=35000&min_price=10000&postal=98087&query=prius%20prime&searchPath=sss&search_distance=100"
urlHtml = "https://seattle.craigslist.org/search/sss?excats=5-2-13-22-2-24-1-4-19-1-1-1-1-1-1-3-6-10-1-1-1-2-2-8-1-1-1-1-1-4-1-7-1-1-1-1-7-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-2-1&max_price=35000&min_price=10000&postal=98087&query=prius%20prime&search_distance=100#search=1~gallery~0~0"


def getLinks():
    [isOk, browser] = seleniumFetcher.getResponse(urlHtml)

    searchBar = browser.find_element(By.TAG_NAME, "input")
    searchBar.send_keys()
    searchBar.send_keys(Keys.RETURN)

    urlList = []
    isNextPage = True
    while isNextPage:
        liList = browser.find_element(
            By.TAG_NAME, "ol").find_elements(By.TAG_NAME, "li")
        for car in liList:
            try:
                tagAlink = car.find_element(By.TAG_NAME, "a")
                carLink = tagAlink.get_attribute("href")
                urlList.append(carLink)
            except selenium.common.exceptions.NoSuchElementException as e:
                
        nextPage = browser.find_element(By.CLASS_NAME, "cl-next-page")
        if nextPage.get_attribute('class').find('disabled') < 0:
            nextPage.click()
        else:
            isNextPage = False
    return urlList


def getCars():
    maxPrice = 35000
    minAutoYear = 2016
    postalSearch = 98087
    # fuel = "pluginhybrid"
    make = "toyota"
    model = "prius prime"
    trim = "advance"

    urlList = getLinks()
    [isOk, soup] = simpleFetcher.getResponse(urlJson)
    if isOk:
        return parse(soup, urlList)
    else:
        return []
