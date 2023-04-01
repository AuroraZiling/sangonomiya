import os

from PyQt6.QtGui import QFont


def getWorkingDir():
    """Returns the working directory of the application"""
    return os.path.abspath(os.curdir).replace("\\", '/')


def getFont(size):
    return QFont("Microsoft YaHei", size)