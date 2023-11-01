
def saveHtml(soup, fileName):
    with open(fileName,'w') as f:
        f.write(str(soup))

def saveString(string, fileName):
    with open(fileName,'w') as f:
        f.write(string)  

def dumpJson(jsonData, fileName):
    with open(fileName,'w') as f:
        json.dump(jsonData, f, indent=2)
