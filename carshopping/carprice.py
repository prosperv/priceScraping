import requests
from bs4 import BeautifulSoup
from price_parser import Price
import re
import json
import plotly.express as px

import carMax
import carshost
import trueCar

sites = [
    carMax,
    carshost,
    trueCar
]

header = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}
def getResponse(url):
    success = True
    response = requests.get(url, headers=header)
    if (response.status_code != 200):
        print("Error got code [{}] with url: {}".format(response.status_code, url))
        success = False
    soup = BeautifulSoup(response.text, 'html.parser')
    return [success, soup]


def saveHtml(soup, fileName):
    with open(fileName,'w') as f:
        f.write(str(soup))

def dumpJson(jsonData, fileName):
    with open(fileName,'w') as f:
        json.dump(jsonData, f, indent=2)

def getModelName(mangledName):
    for filter in carModelNameFilter:
        mangledName = mangledName.replace(filter, '')
    return mangledName.rstrip()

car_header = [
    "make",
    "model",
    "year",
    "price",
    "milage",
    "shippingcost",
    "distance",
    "city",
    "state",
    "vin",
    "link",
    "webhost"
]

def getSubdata(keyValueList, cars):
    subdata = []
    for car in cars:
        addCar = True
        for [key, value] in keyValueList:
            if car[key] != value:
                addCar = False
                break
        if addCar:
            subdata.append(car)
    return subdata


def getlistOfCarsModel(cars):
    setData = set()
    for car in cars:
        setData.add("{} {}".format(car['make'], car['model']))
    return setData




database = []
for site in sites:
    url = site.url
    while url != None:
        print("Processing: {}".format(url))
        [isOk, soup] = getResponse(url)
        myCarDatabase = site.parse(soup)
        database = database + myCarDatabase
        url = site.getNextPage(soup)


#save to file as json
with open("cardatabase.json", 'w') as f:
    json.dump(database, f, indent=2)

print("Cars found:")
print(getlistOfCarsModel(database))
print("Got {} cars".format(len(database)))

fig = px.scatter(database, x='milage', y='price', color='make', symbol='year',
                 title="layout.hovermode='closest' (the default)",
                 hover_name='model', hover_data=["trim", "year", "city", "link"])
# fig = px.scatter(myCarDatabase, x='milage', y='price', color='make', symbol='year',
#                  title="layout.hovermode='closest' (the default)",
#                  hover_name='model', hover_data=["year", "link"])
fig.write_html("final.html", auto_play=True)



print("DONE")
