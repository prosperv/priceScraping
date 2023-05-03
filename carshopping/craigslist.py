import json
from bs4 import BeautifulSoup
import re
from nameParser import *

url = "https://sapi.craigslist.org/web/v8/postings/search/full?batch=2-0-360-0-0&cc=US&lang=en&max_price=32000&min_auto_year=2016&postal=98087&query=(prius%20prime)%20%7C%20phev%20%7C%20(hyundai%20ioniq)%20%7C%20(ford%20c%20max)%20%7C%20(kia%20niro)%20%7C%20(honda%20clarity)%20%7C%20(chevy%20volt)%20%7C%20(chevrolet%20volt)%20%7C%20(((hyundai%20sonata)%20%7C%20(kia%20optima)%20%7C%20(plug%20in))%20hybrid)%20-truck%20-van&searchPath=cta&search_distance=80"
surl = "https://seattle.craigslist.org/search/cta?max_price=32000&min_auto_year=2016&postal=98087&query=(prius%20prime)%20%7C%20phev%20%7C%20(hyundai%20ioniq)%20%7C%20(ford%20c%20max)%20%7C%20(kia%20niro)%20%7C%20(honda%20clarity)%20%7C%20(chevy%20volt)%20%7C%20(chevrolet%20volt)%20%7C%20(((hyundai%20sonata)%20%7C%20(kia%20optima)%20%7C%20(plug%20in))%20hybrid)%20-truck%20-van&search_distance=80"

isHtml = True
isJson = True

def getNextPage(soup):
    return None

def parseFromSelenium(soup):
    souplist = soup.find("div",class_="results cl-results-page cl-search-view-mode-gallery cl-one-column")
    souplist = souplist.find_all("li")

def parse(soup):
    clVehicleId = 145
    database = []
    jsonString = soup[1].text
    data = json.loads(jsonString)['data']
    listings = data['items']

    
    for thing in listings:
        # Filter because craigslist is wierd
        if thing[2] == clVehicleId: 
            print("Price: {}".format(thing[3]))
            c = {
                "make" : "parse",
                "model" : getModelName(8),
                "trim" : name[2],
                "year" : thing['year'],
                "price" : thing['price'],
                "milage" : thing['mileage'],
                "shippingcost" : 0,
                "distance" : None,
                "city" : "",
                "state" : "WA",
                "vin" : thing['vin'],
                "link" : "https://www.cars.com/vehicledetail/{}".format(),
                "webhost" : "cars",
            }
            database.append(c)
    return database