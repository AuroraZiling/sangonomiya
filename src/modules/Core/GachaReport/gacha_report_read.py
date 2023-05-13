import os
import pickle
import time

from ...Scripts.Utils.tools import Tools

utils = Tools()


def getUIDList():
    return os.listdir(f"{utils.workingDir}/data/")


def getDataFromUID(uid):
    if os.path.exists(f"{utils.workingDir}/data/{uid}") and uid:
        return pickle.load(open(f"{utils.workingDir}/data/{uid}/{uid}_data.pickle", 'rb'))
    else:
        return None


def sortDataByTime(data):
    return [i[:-1] for i in sorted(data, key=lambda unit: unit[-1])][::-1]


def convertDataToTable(data):
    categories = {"200": [], "301": [], "302": []}
    copied_categories = {"200": [], "301": [], "302": []}
    for unit in data["list"]:
        categories[unit["uigf_gacha_type"]].append([unit["item_type"], unit["name"], unit["time"]])
        copied_categories[unit["uigf_gacha_type"]].append([unit["item_type"], unit["name"], unit["time"], time.mktime(time.strptime(unit["time"], "%Y-%m-%d %H:%M:%S"))])
    categories["200"] = sortDataByTime(copied_categories["200"])
    categories["301"] = sortDataByTime(copied_categories["301"])
    categories["302"] = sortDataByTime(copied_categories["302"])
    return categories
