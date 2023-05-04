import os
import sys
import shutil
import json
import time
from pathlib import Path
from PyQt6.QtCore import QLocale, QStandardPaths


class Tools:
    def __init__(self):
        self.workingDir = self.getWorkingDir()
        self.OSName = self.getOSName()

    @staticmethod
    def getWorkingDir():
        if sys.platform.startswith("win32"):
            return os.path.abspath(os.curdir).replace("\\", '/')
        elif sys.platform.startswith("darwin"):
            return os.path.dirname(sys.argv[0])

    @staticmethod
    def getOSName() -> str:
        if sys.platform.startswith("win32"):
            return "Windows"
        elif sys.platform.startswith("darwin"):
            return "macOS"
        elif sys.platform.startswith("linux"):
            return "Linux"
        else:
            return "Unknown"

    def getConfigPath(self):
        configPath = str(
            Path(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation))).replace(
            "\\", "/")
        if not os.path.exists(configPath):
            os.mkdir(configPath)
        if not os.path.exists(f"{configPath}/sangonomiya"):
            os.mkdir(f"{configPath}/sangonomiya")
        if self.OSName == "Windows":
            configPath = f"{configPath}/Python/sangonomiya"
        return configPath

    def openFolder(self, path):
        if self.OSName == "Windows":
            os.startfile(path)
        elif self.OSName == "macOS":
            os.system(f"open {path}")

    @staticmethod
    def deleteFiles(filePaths):
        if os.path.exists(filePaths):
            shutil.rmtree(filePaths)
        os.mkdir(filePaths)

    @staticmethod
    def getDirSize(path):
        size = 0
        for root, dirs, files in os.walk(path):
            size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
        return round(size / 1024 / 1024, 2)

    @staticmethod
    def jsonValidator(path, requirement=None):
        if not os.path.exists(path):
            return False
        try:
            file = json.loads(open(path, 'r', encoding="utf-8").read())
            if requirement == "uigf":
                if not file["info"]["uigf_version"] == "v2.2":
                    return False
        except json.decoder.JSONDecodeError:
            return False
        return True

    @staticmethod
    def getFileDate(path):
        return time.strftime("%Y.%m.%d", time.localtime(os.stat(path).st_mtime))