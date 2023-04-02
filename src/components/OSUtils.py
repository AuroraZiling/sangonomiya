import json
import os
from pathlib import Path

import sys

from PyQt6.QtCore import QLocale, QStandardPaths
from PyQt6.QtGui import QFont


def getOSName():
    """Returns the name of the operating system"""
    if sys.platform.startswith("win32"):
        return "Windows"
    elif sys.platform.startswith("darwin"):
        return "MacOS"
    elif sys.platform.startswith("linux"):
        return "Linux"
    else:
        return "Unknown"


def getWorkingDir():
    """Returns the working directory of the application"""
    if sys.platform.startswith("win32"):
        return os.path.abspath(os.curdir).replace("\\", '/')
    elif sys.platform.startswith("darwin"):
        return os.path.dirname(sys.argv[0])


def getLicense():
    """Returns the license of the application"""
    return open(f"{getWorkingDir()}/configs/license", 'r').read()


def getOpenSourceLicense():
    """Returns the open source license of the application"""
    return open(f"{getWorkingDir()}/configs/open_source", 'r').read()


def getAppVersion():
    """Returns the version of the application"""
    return json.loads(open(f"{getWorkingDir()}/configs/application.json", 'r').read())["application_version"]


def getUIVersion():
    """Returns the UI version of the application"""
    return json.loads(open(f"{getWorkingDir()}/configs/application.json", 'r').read())["ui_version"]


def openFolder(path):
    if getOSName() == "Windows":
        os.startfile(path)
    elif getOSName() == "MacOS":
        os.system(f"open {path}")


def getConfigDir():
    path = Path(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation))
    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.exists(path / "sangonomiya"):
        os.mkdir(path / "sangonomiya")
    path = str(path)
    if path.endswith("sangonomiya"):
        path = '/'.join(path.split('/')[:-1])+"/Python"
    return path


def getLanguage():
    with open(f"{getConfigDir()}/sangonomiya/settings.json", 'r') as f:
        tmp = json.loads(f.read())
    return tmp["Customize"]["language"]


def getSystemLanguage():
    return QLocale().system().name()


def getLanguageFiles():
    return [f"{getWorkingDir()}/languages/{getLanguage()}/{f}" for f in
            os.listdir(f"{getWorkingDir()}/languages/{getLanguage()}/") if f.endswith(".qm")]


def getThemeColor():
    if not os.path.exists(f"{getWorkingDir()}/configs/settings.json"):
        return "#009faa"
    return json.loads(open(f"{getWorkingDir()}/configs/settings.json", 'r').read())["Customize"]["themeColor"]


def getFont(size):
    if getOSName() == "Windows":
        return QFont("Microsoft YaHei", size)
    elif getOSName() == "MacOS":
        return QFont("Microsoft YaHei", size + 4)
