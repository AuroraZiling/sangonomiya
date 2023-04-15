# coding:utf-8
import json

import sys

sys.path.append("../../")
from enum import Enum

from qfluentwidgets import (qconfig, QConfig, ConfigItem, OptionsConfigItem,
                            ColorConfigItem, OptionsValidator, EnumSerializer, FolderValidator, BoolValidator)

from components.OSUtils import getWorkingDir, getConfigPath

workingDir = getWorkingDir()
configPath = getConfigPath()
settingsLocal = json.loads(open(f"{workingDir}/configs/application.json", 'r').read())
appVersion, UIVersion = settingsLocal["application_version"], settingsLocal["ui_version"]


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
    storageLogFolders = ConfigItem(
        "Folders", "Log", "logs", FolderValidator())

    # Customize
    customizeLanguage = OptionsConfigItem(
        "Customize", "language", Language.AUTO, OptionsValidator(Language), EnumSerializer(Language), restart=True)
    customizeThemeColor = ColorConfigItem("Customize", "themeColor", "#009faa")
    customizeAutoDeleteLog = ConfigItem("Customize", "autoDeleteLog", False, BoolValidator(), restart=True)



cfg = Config()
qconfig.load(f"{configPath}/settings.json", cfg)