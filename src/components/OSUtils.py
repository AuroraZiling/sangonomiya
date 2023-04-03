import json
import os
from pathlib import Path
import sys
sys.path.append("..")
from PyQt6.QtCore import QLocale, QStandardPaths
from PyQt6.QtGui import QFont



class OSUtils:
    def __init__(self):
        self.OSName = "Unknown"
        self.workingDir = ""
        self.appVersion = "Release 7 Dev 4"
        self.UIVersion = "0.3.1"
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
        if sys.platform.startswith("win32"):
            self.OSName = "Windows"
            self.workingDir = os.path.abspath(os.curdir).replace("\\", '/')
        elif sys.platform.startswith("darwin"):
            self.OSName = "MacOS"
            self.workingDir = os.path.dirname(sys.argv[0])
        elif sys.platform.startswith("linux"):
            self.OSName = "Linux"
        else:
            self.OSName = "Unknown"

        self.license = open(f"{self.workingDir}/configs/license", 'r').read()
        self.openSourceLicense = open(f"{self.workingDir}/configs/open_source", 'r').read()

        if not os.path.exists(self.configPath):
            os.mkdir(self.configPath)
        if not os.path.exists(self.configPath / "sangonomiya"):
            os.mkdir(self.configPath / "sangonomiya")
        self.configPath = str(self.configPath).replace("\\", "/")
        if self.configPath.endswith("sangonomiya"):
            self.configPath = '/'.join(self.configPath.split('/')[:-1]) + "/Python"

        if self.OSName == "Windows":
            self.settings = json.loads(open(f"{self.configPath}/Python/sangonomiya/settings.json", 'r').read())
        elif self.OSName == "MacOS":
            self.settings = json.loads(open(f"{self.configPath}/sangonomiya/settings.json", 'r').read())
        self.settingsLocal = json.loads(open(f"{self.workingDir}/configs/application.json", 'r').read())

        self.appVersion = self.settingsLocal["application_version"]
        self.UIVersion = self.settingsLocal["ui_version"]

        with open(f"{self.configPath}/Python/sangonomiya/settings.json", 'r') as f:
            self.language = json.loads(f.read())["Customize"]["language"]

        self.themeColor = self.settings["Customize"]["themeColor"]

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