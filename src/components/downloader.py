import json

import requests


def downloadFromJson(url, dstDir, dstName):
    try:
        return open(f"{dstDir}/{dstName}", "w", encoding="utf-8").write(
            json.dumps(requests.get(url).json(), indent=4, ensure_ascii=False))
    except requests.exceptions.ConnectionError:
        return open(f"{dstDir}/{dstName}", "w", encoding="utf-8")


def downloadFromImage(url, dstDir, dstName):
    try:
        return open(f"{dstDir}/{dstName}", "wb").write(requests.get(url).content)
    except requests.exceptions.ConnectionError:
        return None
