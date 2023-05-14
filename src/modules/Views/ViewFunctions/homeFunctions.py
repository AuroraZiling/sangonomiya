import json
import os
import requests

from PySide6.QtCore import QThread, Signal

from ...Scripts.Utils import downloader
from ...Scripts.Utils.config_utils import ConfigUtils
from ...constant import SOFTWARE_ANNOUNCEMENT_URL, ANNOUNCE_CURRENT_UP_URL, ANNOUNCE_REQUEST_URL, \
    ANNOUNCE_ICON_REQUEST_URL

utils = ConfigUtils()


class HomeCurrentUPThread(QThread):
    trigger = Signal(int, int, str, str, str)

    def __init__(self, parent=None):
        super(HomeCurrentUPThread, self).__init__(parent)

    def run(self):
        character1ImagePath = f"{utils.workingDir}/assets/unknownAvatar.png"
        character2ImagePath = f"{utils.workingDir}/assets/unknownAvatar.png"
        self.trigger.emit(0, 0, "正在获取信息...", "未知", character1ImagePath)
        self.trigger.emit(0, 1, "正在获取信息...", "未知", character2ImagePath)
        self.trigger.emit(1, 0, "正在获取信息...", "未知", character1ImagePath)
        upWeaponList = []
        if not os.path.exists(f"{utils.workingDir}/cache/announce.json"):
            downloader.downloadFromJson(ANNOUNCE_REQUEST_URL, utils.workingDir + "/cache/", "announce.json")
            downloader.downloadFromJson(ANNOUNCE_ICON_REQUEST_URL, utils.workingDir + "/cache/",
                                        "announce_icons.json")
        downloader.downloadFromJson(ANNOUNCE_CURRENT_UP_URL, utils.workingDir + "/cache/", "current_up.json")
        if os.path.exists(f"{utils.workingDir}/cache/current_up.json") and os.path.exists(f"{utils.workingDir}/cache/announce.json"):
            originalInfo = json.loads(open(f"{utils.workingDir}/cache/current_up.json", 'r', encoding="utf-8").read())["data"]["list"]
            character1Pool = f"{originalInfo[0]['title']} | {originalInfo[0]['content_before_act'].replace('即将概率UP！', '')}"
            character1Time = f"{originalInfo[0]['start_time']} - {originalInfo[0]['end_time']}"
            downloader.downloadFromImage(originalInfo[0]['pool'][0]['icon'], utils.workingDir + "/cache/", "current_up_character_1.png")

            character2Pool = f"{originalInfo[1]['title']} | {originalInfo[1]['content_before_act'].replace('即将概率UP！', '')}"
            character2Time = f"{originalInfo[0]['start_time']} - {originalInfo[0]['end_time']}"
            downloader.downloadFromImage(originalInfo[1]['pool'][0]['icon'], utils.workingDir + "/cache/",
                                         "current_up_character_2.png")

            originalInfo = json.loads(open(f"{utils.workingDir}/cache/announce.json", encoding="utf-8").read())["data"]["list"]
            for announce in originalInfo:
                if "概率UP！" in announce["title"] and "神铸赋形" in announce["title"]:
                    upWeaponList.append(announce["title"].split("：")[1].split("概率UP！")[0])
        else:
            self.trigger.emit(0, 0, "信息获取失败", "未知", character1ImagePath)
            self.trigger.emit(0, 1, "信息获取失败", "未知", character2ImagePath)
            self.trigger.emit(1, 0, "信息获取失败", "未知", character1ImagePath)
            return
        upWeaponList = ' '.join(upWeaponList)
        if os.path.exists(f"{utils.workingDir}/cache/current_up_character_1.png"):
            character1ImagePath = f"{utils.workingDir}/cache/current_up_character_1.png"
        if os.path.exists(f"{utils.workingDir}/cache/current_up_character_2.png"):
            character2ImagePath = f"{utils.workingDir}/cache/current_up_character_2.png"
        self.trigger.emit(0, 0, character1Pool, character1Time, character1ImagePath)
        self.trigger.emit(0, 1, character2Pool, character2Time, character2ImagePath)
        self.trigger.emit(1, 0, "武器: " + ' '.join(upWeaponList), "未知", character1ImagePath)


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
        except requests.exceptions.ConnectionError:
            self.trigger.emit("无网络连接")
            return
        self.trigger.emit(originalInfo)