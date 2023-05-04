

from price_parser import Price
import json
import plotly.express as px

import siteCarMax as siteCarMax
import siteCarsHost as siteCarsHost
import siteTrueCar as siteTrueCar

sites = [
    siteCarMax,
    siteCarsHost,
    siteTrueCar
]


def saveHtml(soup, fileName):
    with open(fileName,'w') as f:
        f.write(str(soup))

def dumpJson(jsonData, fileName):
    with open(fileName,'w') as f:
        json.dump(jsonData, f, indent=2)


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
        setData.add(f"{car['make']} {car['model']}")
    return setData


database = []
for site in sites:
    database = database + site.getCars()
    print(f"Got {len(database)} cars")


#save to file as json
with open("cardatabase.json", 'w') as f:
    json.dump(database, f, indent=2)

print("Cars found:")
print(getlistOfCarsModel(database))
print(f"Got {len(database)} cars")

fig = px.scatter(database, x='milage', y='price', color='make', symbol='year',
                 title="layout.hovermode='closest' (the default)",
                 hover_name='model', hover_data=["trim", "year", "city", "link"])
# fig = px.scatter(myCarDatabase, x='milage', y='price', color='make', symbol='year',
#                  title="layout.hovermode='closest' (the default)",
#                  hover_name='model', hover_data=["year", "link"])
fig.write_html("final.html", auto_play=True)



print("DONE")
