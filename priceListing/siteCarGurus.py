import sys
sys.path.insert(1, '../helper')
import siteHelper

import json

import seleniumFetcher
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

baseUrl = "https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action"

url = "https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?zip=98087&inventorySearchWidgetType=AUTO&fuelTypes=3&maxPrice=30000&installedOptionIds=121&installedOptionIds=139&makeIds=7&sortDir=ASC&sourceContext=untrackedWithinSite_false_0&distance=50&sortType=BEST_MATCH&startYear=2016"
# def getFuelTypeIndex(fuelType:str):
#     if fuelType.lower() == 'hybrid':
#         return 3
#     else:
#         print("Unknown fuel type. Add more fuel type!!")
#         return 3

# # screw this. I don't really need this 
# def buildUrl(filter:dict):
#     if len(filter) == 0:
#         return baseUrl
#     url = baseUrl + '?'
#     if 'fuelType' in filter:
#         url += 'fuelTypes=' + getFuelTypeIndex(filter['fuelType']) + '&'
#     elif 'zip' in filter:
#         url += 'zip=' + str(filter['zip']) + '&'
#     elif 'distance' in filter:
#         url += 'distance=' + str(filter['distance']) = '&'


def parse(soup):
    cars = []
    # parsing the soup
    # find script tag with json data
    constcarscript = soup.find_all("script", string=re.compile("const car")).pop().text

    # Get just the json string
    constcarline = constcarscript.split('\r\n')[1]
    carjsonstring = constcarline.lstrip("const cars = ").rstrip(';')

    rawData= json.loads(carjsonstring)
    for car in rawData:
        c = {
            "make" : car['make'],
            "model" : car['model'],
            "trim" : car['trim'],
            "year" : car['year'],
            "price" : car['basePrice'],
            "milage" : car['mileage'],
            "shippingcost" : car['transferFee'] if car['transferFee'] != None else 0,
            "distance" : None,
            "city" : car['storeName'],
            "state" : car['stateAbbreviation'],
            "vin" : car['vin'],
            "link" : f"https://www.carmax.com/car/{car['stockNumber']}",
            "webhost" : "carmax",
        }
        cars.append(c)
    return cars

def getCars():
    [isOk, browser] = seleniumFetcher.getResponse(url)
    siteHelper.saveString(browser.page_source, "cargurus.html")
    listOf = browser.find_elements(By.TAG_NAME, "script")
    return

