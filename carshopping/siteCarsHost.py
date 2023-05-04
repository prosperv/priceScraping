import json
from simpleFetcher import *
from bs4 import BeautifulSoup
import re
from nameParser import *


jsonUrl = "https://www.cars.com/shopping/results/?dealer_id=&fuel_slugs[]=plug_in_hybrid&keyword=&list_price_max=32000&list_price_min=&makes[]=&maximum_distance=250&mileage_max=&page_size=20&sort=distance&stock_type=all&year_max=&year_min=2016&zip=98087"

def getNextPage(soup):
    return None

def parse(soup):
    database = []
    totalEntries = int(soup.find_all("span","total-entries").pop().text.split()[0])
    dataSiteActivity = soup.find_all("div","sds-page-section listings-page")[0]['data-site-activity']
    vehicleArray = json.loads(dataSiteActivity)['vehicleArray'][1:totalEntries]
    
    for car in vehicleArray:
        name = car['canonical_mmt'].split(":")
        c = {
            "make" : name[0],
            "model" : getModelName(name[1]),
            "trim" : name[2],
            "year" : car['year'],
            "price" : car['price'],
            "milage" : car['mileage'],
            "shippingcost" : 0,
            "distance" : None,
            "city" : "",
            "state" : "WA",
            "vin" : car['vin'],
            "link" : f"https://www.cars.com/vehicledetail/{car['listing_id']}",
            "webhost" : "cars",
        }
        database.append(c)
    return database


def getCars():
    [isOk, soup] = getResponse(jsonUrl)
    if isOk:
        return parse(soup)
