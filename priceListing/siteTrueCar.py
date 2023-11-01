import json
from simpleFetcher import *
from bs4 import BeautifulSoup
import re
from nameParser import *


jsonUrl = "https://workingadvantage.truecar.com/used-cars-for-sale/listings/year-2016-max/body-hatchback/price-below-30000/fuel-plug-in-hybrid/location-lynnwood-wa/"

def getNextPage(soup):
    alink = soup.find_all('a',attrs={"data-qa":"Pagination-directional-next","aria-disabled":"false"})
    if len(alink) == 0:
        return None
    return "https://workingadvantage.truecar.com" + alink[0]['href']

def getListing(root_query):
    theKey = None
    for key in root_query.keys():
        if key.find("BEST_MATCH") != -1:
            theKey = key
            break
    if theKey == None:
        return None
    else:
        return root_query[theKey]['edges']

def parse(soup):
    cars = []
    jsonString = soup.find_all("script",id="__NEXT_DATA__").pop().text
    vehicleArray = json.loads(jsonString)
    root = vehicleArray['props']['pageProps']['__APOLLO_STATE__']
    listings = getListing(root['ROOT_QUERY'])
    for car in listings:
        listingId = car['node']['__ref']
        listing = root[listingId]
        vehicle = listing['vehicle']
        # print(vehicle)
        transferFee = listing['pricing']['transferFee']
        parentDealership = root[listing['dealership']['__ref']]['parentDealershipName']
        c = {
            "make" : root[vehicle['make']['__ref']]['name'],
            "model" : getModelName(root[vehicle['model']['__ref']]['name']),
            "trim" : root[vehicle['style']['__ref']]['name'],
            "year" : vehicle['year'],
            "price" : listing['pricing']['listPrice'],
            "milage" : vehicle['mileage'],
            "shippingcost" : 0 if transferFee == None else transferFee['amount'],
            "distance" : None if transferFee == None else transferFee['distance'],
            "city" : "" if transferFee == None else transferFee['fromCity'],
            "state" : "" if transferFee == None else transferFee['fromState'],
            "vin" : vehicle['vin'],
            "link" : f"https://workingadvantage.truecar.com/used-cars-for-sale/listing/{vehicle['vin']}",
            "webhost" : "trueCars" if parentDealership == None else parentDealership,
        }
        cars.append(c)
    return cars

def getCars():
    cars = []
    url = jsonUrl
    while url != None:
        print(f"Processing: {url}")
        [isOk, soup] = getResponse(url)
        if isOk:
            cars = cars + parse(soup)
            url = getNextPage(soup)
    return cars
