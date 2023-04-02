# coding:utf-8
import os.path
from pathlib import Path

import sys
sys.path.append("..")
from enum import Enum

from qfluentwidgets import (qconfig, QConfig, ConfigItem, OptionsConfigItem, BoolValidator,
                            ColorConfigItem, OptionsValidator, RangeConfigItem, RangeValidator,
                            FolderListValidator, EnumSerializer, FolderValidator)

from components import OSUtils

WORKING_DIR = OSUtils.getWorkingDir()
CONFIG_DIR = OSUtils.getConfigDir()


class Language(Enum):
    """ Language enumeration """

    CHINESE_SIMPLIFIED = "zh_CN"
    ENGLISH = "en_US"
    AUTO = "Auto"


class Config(QConfig):
    """ Config of application """

    # Storage
    storageDataFolders = ConfigItem(
        "Folders", "Data", "data", FolderValidator())
    storageCacheFolders = ConfigItem(
        "Folders", "Cache", "cache", FolderValidator())

    # Customize
    customizeLanguage = OptionsConfigItem(
        "Customize", "language", Language.AUTO, OptionsValidator(Language), EnumSerializer(Language), restart=True)
    customizeThemeColor = ColorConfigItem("Customize", "themeColor", '#009faa')


cfg = Config()
qconfig.load(f"{CONFIG_DIR}/Python/sangonomiya/settings.json", cfg)