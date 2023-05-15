
carModelNameFilter = [
    "Plug-In-Hybrid",
    "Plug-in Hybrid",
    "Plug-In Hybrid",
    "Plug in Hybrid",
    "Plug-in",
    "Plug In",
    "Plug in",
    "Hybrid",
]

nameReplaceFilter = [
    ['IONIQ', "Ioniq"]
]

def getModelName(mangledName):
    for filter in carModelNameFilter:
        mangledName = mangledName.replace(filter, '')
    for [wrongName, rightName] in nameReplaceFilter:
        mangledName = mangledName.replace(wrongName, rightName)
    return mangledName.rstrip()

makers = [
    "Toyota",
    "Hyundai",
    "Ford",
    "Kia",
    "Honda",
    "Chevy",
    "Chevrolet",
]


def findMakerName(mangledName):
    lowerMangledname = mangledName.lower()
    for maker in makers:
        lowerMaker = maker.lower()
        if (lowerMangledname.find(lowerMaker) >= 0):
            if (maker == "Chevy"):
                return "Chevrolet"
            return maker
    return ""


modelCorrections = [
    ('Prime', ["prime"]),
    ('Volt', ["volt"]),
    ('Ioniq', ["ioniq"]),
    ('C-Max', ["c-max", "c max"]),
    ('Niro', ["niro"]),
]


def findModelName(mangledName):
    lowerMangledname = mangledName.lower()
    for [model, potentialNames] in modelCorrections:
        for name in potentialNames:
            if (lowerMangledname.find(name) >= 0):
                return model
    return ""


def findYear(mangledName, minYear):
    for year in range(minYear, 2023):
        if (mangledName.find(str(year)) >= 0):
            return year
    return ""
