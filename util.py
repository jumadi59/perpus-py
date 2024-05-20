import json
import os
from datetime import datetime

rootPath = os.getcwd() + "/"

def incrementId(fileName):
    increment = openData("data/increment.json")
    
    if len(increment) != 0:increment[fileName] = increment[fileName]+1
    else:
        increment = {fileName: 0}

    with open(rootPath + "data/increment.json", "w") as file:
        json.dump(increment, file)
    return increment[fileName]


def openData(fileName):
    filePath = rootPath + fileName
    if os.path.exists(filePath) == False: return []
   
    with open(filePath, "r") as file:
        data = json.load(file)
    
    return data

def addData(fileName, item):
    data = openData(fileName)
    item["id"] = incrementId(fileName)
    data.append(item)

    filePath = rootPath + fileName
    with open(filePath, "w") as file:
        json.dump(data, file)

def updateData(fileName, item):
    data = openData(fileName)
    update = []
    for it in data:
        if it["id"] == item["id"]:
            update.append(item)
        else:
            update.append(it)

    filePath = rootPath + fileName
    with open(filePath, "w") as file:
        json.dump(update, file)

def getData(fileName, key, value):
    items = openData(fileName)
    for item in items:
        if item[key] == value:
            return item
    return None


def removeData(fileName, item):
    data = openData(fileName)
    data = [it for it in data if it["id"] != item["id"]]

    filePath = rootPath + fileName
    with open(filePath, "w") as file:
        json.dump(data, file)

def getItemList(list, index):
    arr = []
    for item in list:
        arr.append(item[index])
    return arr

def formatrupiah(uang):
    y = str(uang)
    if len(y) <= 3:
        return 'Rp ' + y
    else:
        p = y[-3:]
        q = y[:-3]
        return formatrupiah(q) + '.' + p

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

def hitungTelatBayar(tglPengembalian):
    dtPengembalian = datetime.strptime(tglPengembalian, "%d-%m-%Y")
    dtNow = datetime.now()
    dtTelat = (dtNow - dtPengembalian).days
    if dtTelat > 0: return dtTelat 
    else: return 0
