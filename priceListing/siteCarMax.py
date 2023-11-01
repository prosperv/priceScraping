import json
from simpleFetcher import *
from bs4 import BeautifulSoup
import re
from nameParser import *

jsonUrl = "https://www.carmax.com/cars/plug-in-hybrid?year=2016-2023&price=35000"
jsonUrl = "https://www.carmax.com/cars/plug-in-hybrid?year=2016-2023&price=35000"


def getNextPage(soup):
    return None


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
            "model" : getModelName(car['model']),
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
    [isOk, soup] = getResponse(jsonUrl)
    if isOk:
        return parse(soup)
