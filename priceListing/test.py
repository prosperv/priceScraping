import sys
sys.path.insert(1, '../helper')

import siteCarGurus as siteCarGurus

site = 'cargurus'

filter = {
    'maxPrice' : 35000,
    'minAutoYear' : 2016,
    'postalSearch' : 98087,
    'distance' : 100,
    'fuel' : "pluginhybrid",
    'make' : "toyota",
    'model' : "prius prime",
    'trim' : "advance",
}

cars = siteCarGurus.getCars()