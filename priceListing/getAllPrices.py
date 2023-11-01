import priceListing.siteCarGurus as siteCarGurus

sites = [
    siteCarGurus
]


database = []
for site in sites:
    database += site.getCars()
    print(f"Got {len(database)} cars")


#save to file as json
with open("cardatabase.json", 'w') as f:
    json.dump(database, f, indent=2)