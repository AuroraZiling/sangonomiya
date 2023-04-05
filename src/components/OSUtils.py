import json
import os
from pathlib import Path
import sys

sys.path.append("..")
from PyQt6.QtCore import QLocale, QStandardPaths
from PyQt6.QtGui import QFont


ANNOUNCE_REQUEST_URL = "https://hk4e-api-static.mihoyo.com/common/hk4e_cn/announcement/api/getAnnContent?game=hk4e&game_biz=hk4e_cn&lang=zh-cn&bundle_id=hk4e_cn&platform=pc&region=cn_gf01&level=60&channel_id=1"
ANNOUNCE_ICON_REQUEST_URL = "https://hk4e-api.mihoyo.com/common/hk4e_cn/announcement/api/getAnnList?game=hk4e&game_biz=hk4e_cn&lang=zh-cn&auth_appid=announcement&authkey_ver=1&bundle_id=hk4e_cn&channel_id=1&level=60&platform=pc&region=cn_gf01&sdk_presentation_style=fullscreen&sdk_screen_transparent=true&sign_type=2&uid=1"
HTML_MODEL = '''
<!DOCTYPE html>
<html>
  <head>
  <body style="background-color:#272727;"></body>
  </head>
  <body>
    {content}
  </body>
</html>
'''


def getWorkingDir():
    if sys.platform.startswith("win32"):
        return os.path.abspath(os.curdir).replace("\\", '/')
    elif sys.platform.startswith("darwin"):
        return os.path.dirname(sys.argv[0])


def getOSName():
    if sys.platform.startswith("win32"):
        return "Windows"
    elif sys.platform.startswith("darwin"):
        return "MacOS"
    elif sys.platform.startswith("linux"):
        return "Linux"
    else:
        return "Unknown"


def getConfigPath(OSName=getOSName()):
    configPath = str(Path(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation))).replace("\\", "/")
    if not os.path.exists(configPath):
        os.mkdir(configPath)
    if not os.path.exists(f"{configPath}/sangonomiya"):
        os.mkdir(f"{configPath}/sangonomiya")
    if OSName == "Windows":
        configPath = f"{configPath}/Python/sangonomiya"
    return configPath


class OSUtils:
    def __init__(self):
        self.OSName = "Unknown"
        self.workingDir = ""
        self.appVersion = "Release 7 Dev 4"
        self.UIVersion = "0.5.7"
        self.license = "Unknown"
        self.openSourceLicense = "Unknown"
        self.configPath = Path(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation))
        self.language = "Auto"
        self.systemLanguage = QLocale().system().name()
        self.languageFiles = []
        self.themeColor = "#009faa"

        self.settings = {}

        self.__config()

    def __config(self):

        self.workingDir = getWorkingDir()
        self.OSName = getOSName()
        self.configPath = getConfigPath()

        self.license = open(f"{self.workingDir}/configs/license", 'r').read()
        self.openSourceLicense = open(f"{self.workingDir}/configs/open_source", 'r').read()

        if os.path.exists(f"{self.configPath}/Python/sangonomiya/settings.json") or os.path.exists(
                f"{self.configPath}/sangonomiya/settings.json"):
            if self.OSName == "Windows":
                self.settings = json.loads(open(f"{self.configPath}/Python/sangonomiya/settings.json", 'r').read())
            elif self.OSName == "MacOS":
                self.settings = json.loads(open(f"{self.configPath}/sangonomiya/settings.json", 'r').read())
            with open(f"{self.configPath}/Python/sangonomiya/settings.json", 'r') as f:
                self.language = json.loads(f.read())["Customize"]["language"]
        self.settingsLocal = json.loads(open(f"{self.workingDir}/configs/application.json", 'r').read())

        self.appVersion = self.settingsLocal["application_version"]
        self.UIVersion = self.settingsLocal["ui_version"]

    def openFolder(self, path):
        if self.OSName == "Windows":
            os.startfile(path)
        elif self.OSName == "MacOS":
            os.system(f"open {path}")

    def getFont(self, size):
        if self.OSName == "Windows":
            return QFont("Microsoft YaHei", size)
        elif self.OSName == "MacOS":
            return QFont("Microsoft YaHei", size + 6)


    @staticmethod
    def getAnnounceRequestURL():
        return ANNOUNCE_REQUEST_URL

    @staticmethod
    def getAnnounceIconRequestURL():
        return ANNOUNCE_ICON_REQUEST_URL

    def getAnnounceData(self):
        return json.loads(open(f"{self.workingDir}/cache/announce.json", 'r', encoding="utf-8").read())

    def getAnnounceIconData(self):
        return json.loads(open(f"{self.workingDir}/cache/announce_icons.json", 'r', encoding="utf-8").read())

    def deleteAllLogFiles(self):
        logDir = os.listdir(f"{self.workingDir}/logs")
        for eachLogFile in logDir:
            try:
                os.remove(f"{self.workingDir}/logs/{eachLogFile}")
            except PermissionError:
                continue
