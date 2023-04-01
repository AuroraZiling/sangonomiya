import json
import os
import sys

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


def getFont(size):
    return QFont("Microsoft YaHei", size)
