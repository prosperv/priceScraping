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
                    "make": findMakerName(thing[8]),  # parse
                    "model": findModelName(thing[8]),  # parse
                    "trim": "",
                    "year": findYear(thing[8], 2010),
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


urlJson = "https://sapi.craigslist.org/web/v8/postings/search/full?batch=2-0-360-0-0&cc=US&lang=en&max_price={}&min_auto_year={}&postal={}&purveyor=owner&query={}&searchPath=cta&search_distance=80"
urlHtml = "https://seattle.craigslist.org/search/cta?max_price={}&min_auto_year={}&postal={}&purveyor=owner&search_distance=80"


def getLinks(maxPrice, minAutoYear, postalSearch, queryString):
    [isOk, browser] = seleniumFetcher.getResponse(
        urlHtml.format(maxPrice, minAutoYear, postalSearch))

    searchBar = browser.find_element(By.TAG_NAME, "input")
    searchBar.send_keys(queryString)
    searchBar.send_keys(Keys.RETURN)

    urlList = []
    isNextPage = True
    while isNextPage:
        liList = browser.find_element(
            By.TAG_NAME, "ol").find_elements(By.TAG_NAME, "li")
        for car in liList:
            urlList.append(car.find_element(
                By.TAG_NAME, "a").get_attribute("href"))
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

    queryString = "(prius prime)|(chevy volt)|(chevrolet volt)|(hyundai ioniq)|(ford c max)|(kia niro)"

    urlList = getLinks(maxPrice, minAutoYear, postalSearch, queryString)
    [isOk, soup] = simpleFetcher.getResponse(
        urlJson.format(maxPrice, minAutoYear, postalSearch, urllib.parse.quote(queryString)))
    if isOk:
        return parse(soup, urlList)
