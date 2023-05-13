import os
import pickle

from ...Scripts.Utils.tools import Tools

utils = Tools()


def getUIDList():
    return os.listdir(f"{utils.workingDir}/data/")


def getDataFromUID(uid):
    if os.path.exists(f"{utils.workingDir}/data/{uid}") and uid:
        return pickle.load(open(f"{utils.workingDir}/data/{uid}/{uid}_data.pickle", 'rb'))
    else:
        return None


def convertDataToTable(data):
    categories = {"200": [], "301": [], "302": []}
    for unit in data["list"]:
        categories[unit["uigf_gacha_type"]].append([unit["item_type"], unit["name"], unit["time"]])
    return categories
