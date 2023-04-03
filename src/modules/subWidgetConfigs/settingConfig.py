# coding:utf-8
import json
from pathlib import Path

import sys
from PyQt6.QtCore import QStandardPaths

sys.path.append("../../")
from enum import Enum
import os

from qfluentwidgets import (qconfig, QConfig, ConfigItem, OptionsConfigItem, BoolValidator,
                            ColorConfigItem, OptionsValidator, RangeConfigItem, RangeValidator,
                            FolderListValidator, EnumSerializer, FolderValidator)

if sys.platform.startswith("win32"):
    workingDir = os.path.abspath(os.curdir).replace("\\", '/')
elif sys.platform.startswith("darwin"):
    workingDir = os.path.dirname(sys.argv[0])

configPath = Path(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation))
if not os.path.exists(configPath):
    os.mkdir(configPath)
if not os.path.exists(configPath / "sangonomiya"):
    os.mkdir(configPath / "sangonomiya")
configPath = str(configPath)
if configPath.endswith("sangonomiya"):
    configPath = '/'.join(configPath.split('/')[:-1]) + "/Python"
settingsLocal = json.loads(open(f"{workingDir}/configs/application.json", 'r').read())
appVersion = settingsLocal["application_version"]
UIVersion = settingsLocal["ui_version"]


class Language(Enum):
    """ Language enumeration """

    CHINESE_SIMPLIFIED = "zh_CN"
    ENGLISH = "en_US"
    AUTO = "Auto"


class Config(QConfig):
    """ Config of application """

    # General
    ConfigItem("Versions", "application", appVersion)
    ConfigItem("Versions", "ui", UIVersion)

    # Storage
    storageDataFolders = ConfigItem(
        "Folders", "Data", "data", FolderValidator())
    storageCacheFolders = ConfigItem(
        "Folders", "Cache", "cache", FolderValidator())

    # Customize
    customizeLanguage = OptionsConfigItem(
        "Customize", "language", Language.AUTO, OptionsValidator(Language), EnumSerializer(Language), restart=True)
    customizeThemeColor = ColorConfigItem("Customize", "themeColor", "#009faa")


cfg = Config()
qconfig.load(f"{configPath}/Python/sangonomiya/settings.json", cfg)