import requests

DEV_URL = "https://raw.githubusercontent.com/AuroraZiling/sangonomiya.Metadata/main/dev.json"


def findLatestVersion():
    return requests.get(DEV_URL).json()


def compareVersion(current, target):
    if "Dev" in current and "Dev" in target:
        return True if int(target[-1]) > int(current[-1]) else False