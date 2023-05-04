import json
import time

import requests
import sys

sys.path.append("../../..")

from modules.Scripts.Utils import logTracker as log


def getResponse(url):
    """
    Get the response from server

    :param url: str
    """
    return requests.get(url, timeout=2)


def downloadFromJson(url, dstDir, dstName):
    """
    Download .json file from server

    :param url(str), dstDir(str), dstName(str), sync(bool)[optional=False]
    :return response: IO
    """
    timeStart = time.time()
    log.infoWrite(f"[Component][Downloader] Trying to get JSON file from {url} in sync mode")
    jsonData = requests.get(url)
    if jsonData:
        log.infoWrite(f"[Component][Downloader] The JSON file has been successfully downloaded and stored in {dstDir}/{dstName} (Time consumption: {time.time()-timeStart}s)")
        return open(f"{dstDir}/{dstName}", "w", encoding="utf-8").write(
            json.dumps(jsonData.json(), indent=4, ensure_ascii=False))
    log.errorWrite(f"[Component][Downloader] JSON file download failed ({url})")
    return open(f"{dstDir}/{dstName}", "w", encoding="utf-8")


def downloadFromImage(url, dstDir, dstName):
    """
    Download image file from server

    :param url(str), dstDir(str), dstName(str), sync(bool)[optional=False]
    :return response: IO, None
    """
    timeStart = time.time()
    log.infoWrite(f"[Component][Downloader] Trying to get image from {url} in sync mode")
    imageData = requests.get(url)
    if imageData:
        log.infoWrite(f"[Component][Downloader] The image has been successfully downloaded and stored in {dstDir}/{dstName} (Time consumption: {time.time()-timeStart}s)")
        return open(f"{dstDir}/{dstName}", "wb").write(imageData.content)
    log.errorWrite(f"[Component][Downloader] image download failed ({url})")
    return None
