import json
import os
import pathlib
import shutil
import sys

sys.path.append("../../..")
from PyQt6.QtCore import QLocale
from PyQt6.QtGui import QFont
from ..Utils.tools import Tools

ANNOUNCE_REQUEST_URL = "https://hk4e-api-static.mihoyo.com/common/hk4e_cn/announcement/api/getAnnContent?game=hk4e&game_biz=hk4e_cn&lang=zh-cn&bundle_id=hk4e_cn&platform=pc&region=cn_gf01&level=60&channel_id=1"
ANNOUNCE_ICON_REQUEST_URL = "https://hk4e-api.mihoyo.com/common/hk4e_cn/announcement/api/getAnnList?game=hk4e&game_biz=hk4e_cn&lang=zh-cn&auth_appid=announcement&authkey_ver=1&bundle_id=hk4e_cn&channel_id=1&level=60&platform=pc&region=cn_gf01&sdk_presentation_style=fullscreen&sdk_screen_transparent=true&sign_type=2&uid=1"
HTML_MODEL = '''
<!DOCTYPE html>
<html>
  <head>
  <style>
    body::-webkit-scrollbar {display: none;}
    {css}
  </style>
  </head>
  <body style="background-color: transparent;">
    <article class="markdown-body" style="background-color: transparent;">
        {content}
    </article>
  </body>
</html>
'''


class ConfigUtils(Tools):
    def __init__(self):
        super().__init__()
        self.OSName = super().getOSName()
        self.workingDir = super().getWorkingDir()
        self.license = open(f"{self.workingDir}/assets/configs/license", 'r').read()
        self.openSourceLicense = open(f"{self.workingDir}/assets/configs/open_source", 'r').read()
        self.configPath = super().getConfigPath()
        self.language = "Auto"
        self.systemLanguage = QLocale().system().name()
        self.languageFiles = []
        self.themeColor = "#009faa"
        self.accountInfo = {}

        self.settings = {}
        self.appVersion = "Unknown"
        self.UIVersion = "Unknown"

        self.__fileCheck()
        self.__settings()

    def __fileCheck(self):
        pathlib.Path(self.configPath).mkdir(parents=True, exist_ok=True)
        if not os.path.exists(f"{self.configPath}/account.json"):
            shutil.copyfile(f"{self.workingDir}/assets/configs/modelFiles/account.json",
                            f"{self.configPath}/account.json")

    def __settings(self):
        if os.path.exists(f"{self.configPath}/settings.json"):
            self.settings = json.loads(open(f"{self.configPath}/settings.json", 'r').read())
            with open(f"{self.configPath}/settings.json", 'r') as f:
                self.language = json.loads(f.read())["Customize"]["language"]
        self.settingsLocal = json.loads(open(f"{self.workingDir}/assets/configs/application.json", 'r').read())
        self.accountInfo = json.loads(open(f"{self.configPath}/account.json", 'r', encoding="utf-8").read())
        self.appVersion = self.settingsLocal["application_version"]
        self.UIVersion = self.settingsLocal["ui_version"]

    def getFont(self, size):
        if self.OSName == "Windows":
            return QFont("Microsoft YaHei", size)
        elif self.OSName == "macOS":
            return QFont("Microsoft YaHei", size + 6)

    def getConfigAutoDeleteLog(self):
        try:
            with open(f"{self.configPath}/settings.json", 'r') as f:
                return json.loads(f.read())["Customize"]["autoDeleteLog"]
        except KeyError:
            return False
        except FileNotFoundError:
            return False

    def getAnnounceData(self):
        try:
            return json.loads(open(f"{self.workingDir}/cache/announce.json", 'r', encoding="utf-8").read())
        except json.decoder.JSONDecodeError:
            return None

    def getAnnounceIconData(self):
        try:
            return json.loads(open(f"{self.workingDir}/cache/announce_icons.json", 'r', encoding="utf-8").read())
        except json.decoder.JSONDecodeError:
            return None

    def deleteAllLogFiles(self):
        logDir = os.listdir(f"{self.workingDir}/logs")
        for eachLogFile in logDir:
            try:
                os.remove(f"{self.workingDir}/logs/{eachLogFile}")
            except PermissionError:
                continue

    def deleteAllCacheFiles(self):
        logDir = os.listdir(f"{self.workingDir}/cache")
        for eachLogFile in logDir:
            try:
                os.remove(f"{self.workingDir}/cache/{eachLogFile}")
            except PermissionError:
                continue

    def getAccountUid(self):
        self.accountInfo = json.loads(open(f"{self.configPath}/account.json", 'r', encoding="utf-8").read())
        return self.accountInfo["uid"]

    def getAccountName(self):
        self.accountInfo = json.loads(open(f"{self.configPath}/account.json", 'r', encoding="utf-8").read())
        return self.accountInfo["name"]

    def getVersionType(self):
        return "dev" if "Dev" in self.appVersion else "release"

    def getLanguage(self):
        return self.language

    @staticmethod
    def getHTMLMODEL():
        return HTML_MODEL

    @staticmethod
    def getAnnounceIconRequestURL():
        return ANNOUNCE_ICON_REQUEST_URL

    @staticmethod
    def getAnnounceRequestURL():
        return ANNOUNCE_REQUEST_URL
