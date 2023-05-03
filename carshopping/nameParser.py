
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