import json
import os
import requests

from PySide6.QtCore import QThread, Signal

from ...Scripts.Utils import downloader
from ...Scripts.Utils.config_utils import ConfigUtils
from ...constant import SOFTWARE_ANNOUNCEMENT_URL, ANNOUNCE_ICON_REQUEST_URL, ANNOUNCE_REQUEST_URL

utils = ConfigUtils()


class HomeCurrentUPThread(QThread):
    trigger = Signal(int, str)

    def __init__(self, parent=None):
        super(HomeCurrentUPThread, self).__init__(parent)

    def run(self):
        self.trigger.emit(0, "正在获取信息...")
        self.trigger.emit(1, "正在获取信息...")
        upCharacterList, upWeaponList = [], []
        if not os.path.exists(f"{utils.workingDir}/cache/announce.json"):
            downloader.downloadFromJson(ANNOUNCE_REQUEST_URL, utils.workingDir + "/cache/", "announce.json")
            downloader.downloadFromJson(ANNOUNCE_ICON_REQUEST_URL, utils.workingDir + "/cache/",
                                        "announce_icons.json")
        if os.path.exists(f"{utils.workingDir}/cache/announce.json"):
            originalInfo = json.loads(open(f"{utils.workingDir}/cache/announce.json", encoding="utf-8").read())["data"]["list"]
            for announce in originalInfo:
                if "概率UP！" in announce["title"] and "神铸赋形" not in announce["title"]:
                    upCharacterList.append(announce["title"].split("：")[1].split("概率UP！")[0])
                if "概率UP！" in announce["title"] and "神铸赋形" in announce["title"]:
                    upWeaponList.append(announce["title"].split("：")[1].split("概率UP！")[0])
        else:
            self.trigger.emit(0, "信息获取失败")
            self.trigger.emit(1, "信息获取失败")
            return
        upCharacterList = ' '.join(upCharacterList)
        upWeaponList = ' '.join(upWeaponList)
        self.trigger.emit(0, upCharacterList)
        self.trigger.emit(1, upWeaponList)


class HomeSoftwareAnnouncementThread(QThread):
    trigger = Signal(str)

    def __init__(self, parent=None):
        super(HomeSoftwareAnnouncementThread, self).__init__(parent)

    def run(self):
        self.trigger.emit("正在获取公告...")
        try:
            originalInfo = requests.get(SOFTWARE_ANNOUNCEMENT_URL).text
        except requests.exceptions.SSLError:
            self.trigger.emit("公告获取失败")
            return
        self.trigger.emit(originalInfo)