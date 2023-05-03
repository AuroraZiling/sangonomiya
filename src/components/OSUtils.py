import json
import os
import shutil
import time
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


def getWorkingDir() -> str:
    """
    Get the directory where the script running.

    Returns: (str) the parent directory where script running.
        E.g. /Users/Username/Program/sangonomiya/src (in macOS)
    """
    if sys.platform.startswith("win32"):
        return os.path.abspath(os.curdir).replace("\\", '/')
    elif sys.platform.startswith("darwin"):
        return os.path.dirname(sys.argv[0])


def getOSName() -> str:
    """
    Get the name of operating system.

    Returns: (str) the OS Name
       Values are Windows, macOS, Linux, Unknown
    """
    if sys.platform.startswith("win32"):
        return "Windows"
    elif sys.platform.startswith("darwin"):
        return "macOS"
    elif sys.platform.startswith("linux"):
        return "Linux"
    else:
        return "Unknown"


def getConfigPath(OSName=getOSName()):
    """
    Get the directory where the configuration file is located.

    Returns: (str) the path
        E.g. /Users/Username/Library/Application Support (in macOS)
    """
    configPath = str(Path(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation))).replace(
        "\\", "/")
    if not os.path.exists(configPath):
        os.mkdir(configPath)
    if not os.path.exists(f"{configPath}/sangonomiya"):
        os.mkdir(f"{configPath}/sangonomiya")
    if OSName == "Windows":
        configPath = f"{configPath}/Python/sangonomiya"
    return configPath


def getConfigAutoDeleteLog():
    """
    Get the directory where the configuration file is located.

    Returns: (str) the path
        E.g. /Users/Username/Library/Application Support (in macOS)
    """
    try:
        with open(f"{getConfigPath(getOSName())}/settings.json", 'r') as f:
            return json.loads(f.read())["Customize"]["autoDeleteLog"]
    except KeyError:
        return False
    except FileNotFoundError:
        return False


def deleteFiles(filePaths):
    if os.path.exists(filePaths):
        shutil.rmtree(filePaths)
    os.mkdir(filePaths)


class OSUtils:
    def __init__(self):
        self.OSName = "Unknown"
        self.workingDir = ""
        self.appVersion = "Release 7 Dev 4"
        self.UIVersion = ""
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

        self.accountInfo = json.loads(open(f"{self.configPath}/account.json", 'r', encoding="utf-8").read())
        self.license = open(f"{self.workingDir}/configs/license", 'r').read()
        self.openSourceLicense = open(f"{self.workingDir}/configs/open_source", 'r').read()

        if os.path.exists(f"{self.configPath}/settings.json"):
            self.settings = json.loads(open(f"{self.configPath}/settings.json", 'r').read())
            with open(f"{self.configPath}/settings.json", 'r') as f:
                self.language = json.loads(f.read())["Customize"]["language"]
        self.settingsLocal = json.loads(open(f"{self.workingDir}/configs/application.json", 'r').read())

        self.appVersion = self.settingsLocal["application_version"]
        self.UIVersion = self.settingsLocal["ui_version"]

    def openFolder(self, path):
        if self.OSName == "Windows":
            os.startfile(path)
        elif self.OSName == "macOS":
            os.system(f"open {path}")

    def getFont(self, size):
        if self.OSName == "Windows":
            return QFont("Microsoft YaHei", size)
        elif self.OSName == "macOS":
            return QFont("Microsoft YaHei", size + 6)

    @staticmethod
    def getAnnounceRequestURL():
        return ANNOUNCE_REQUEST_URL

    @staticmethod
    def getAnnounceIconRequestURL():
        return ANNOUNCE_ICON_REQUEST_URL

    @staticmethod
    def getDirSize(path):
        size = 0
        for root, dirs, files in os.walk(path):
            size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
        return round(size / 1024 / 1024, 2)

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

    @staticmethod
    def jsonValidator(path):
        if not os.path.exists(path):
            return False
        try:
            json.loads(open(path, 'r', encoding="utf-8").read())
        except json.decoder.JSONDecodeError:
            return False
        return True

    @staticmethod
    def getFileDate(path):
        return time.strftime("%Y.%m.%d", time.localtime(os.stat(path).st_mtime))
