
# import siteCarGurus as siteCarGurus
import siteCarMax as siteCarMax
import siteCarsHost as siteCarsHost
import siteCraigslist as siteCraigslist
import siteTrueCar as siteTrueCar


import json
import plotly.express as px

    # siteCarGurus,
sites = [
    siteCraigslist,
    # siteCarMax,
    # siteCarsHost,
    # siteTrueCar,
]

def getlistOfCarsModel(cars):
    setData = set()
    for car in cars:
        setData.add(f"{car['make']} {car['model']}")
    return setData

database = []
for site in sites:
    database += site.getCars()
    print(f"Got {len(database)} cars")


#save to file as json
with open("cardatabase.json", 'w') as f:
    json.dump(database, f, indent=2)
    

print("Cars found:")
print(getlistOfCarsModel(database))
print(f"Got {len(database)} cars")

# Draw graph
fig = px.scatter(database, x='milage', y='price', color='make', symbol='year',
                 title="layout.hovermode='closest' (the default)",
                 hover_name='model', hover_data=["trim", "year", "city", "link"])
# fig = px.scatter(myCarDatabase, x='milage', y='price', color='make', symbol='year',
#                  title="layout.hovermode='closest' (the default)",
#                  hover_name='model', hover_data=["year", "link"])

fig.write_html("final.html", auto_play=True)

