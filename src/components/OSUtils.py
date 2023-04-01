import os
import sys

from PyQt6.QtGui import QFont


def getWorkingDir():
    """Returns the working directory of the application"""
    if sys.platform.startswith("win32"):
        return os.path.abspath(os.curdir).replace("\\", '/')
    elif sys.platform.startswith("darwin"):
        return os.path.dirname(sys.argv[0])


def getFont(size):
    return QFont("Microsoft YaHei", size)