# coding:utf-8
import sys

sys.path.append("..")

from modules.subWidgetConfigs import settingConfig
from components import OSUtils, customIcon, infoBars
from components import logTracker as log
from qfluentwidgets import (SettingCardGroup, PushSettingCard, ScrollArea,
                            ComboBoxSettingCard, ExpandLayout, isDarkTheme, Dialog)
from qfluentwidgets import FluentIcon
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QLabel

cfg = settingConfig.cfg
utils = OSUtils.OSUtils()


class SettingWidget(ScrollArea):
    checkUpdateSig = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)
        self.settingLabel = QLabel(self.tr("Settings"), self)

        self.configPath = utils.configPath

        # Storage
        self.storageGroup = SettingCardGroup(self.tr("Storage"), self.scrollWidget)
        self.storageDataCard = PushSettingCard(
            self.tr("Open"),
            FluentIcon.FOLDER,
            self.tr("Data Folder"),
            cfg.get(cfg.storageDataFolders),
            self.storageGroup
        )
        self.storageCacheCard = PushSettingCard(
            self.tr("Open"),
            FluentIcon.FOLDER,
            self.tr("Cache Folder"),
            cfg.get(cfg.storageCacheFolders),
            self.storageGroup
        )
        self.storageLogCard = PushSettingCard(
            self.tr("Open"),
            FluentIcon.FOLDER,
            self.tr("Log Folder"),
            cfg.get(cfg.storageLogFolders),
            self.storageGroup
        )
        self.storageConfigCard = PushSettingCard(
            self.tr("Open"),
            FluentIcon.FOLDER,
            self.tr("Config Folder"),
            self.configPath,
            self.storageGroup
        )

        # Default

        self.defaultGroup = SettingCardGroup(self.tr("Default"), self.scrollWidget)

        self.defaultLogDeleteCard = PushSettingCard(
            self.tr("Delete"),
            customIcon.MyFluentIcon.DELETE,
            self.tr("Delete all log files"),
            f"All logs in {utils.workingDir + '/logs'} will be deleted",
            self.defaultGroup
        )

        # Customize
        self.customizeGroup = SettingCardGroup(self.tr("Customize"), self.scrollWidget)

        self.customizeLanguageSetting = ComboBoxSettingCard(
            cfg.customizeLanguage,
            FluentIcon.LANGUAGE,
            self.tr("Language"),
            self.tr("Set the language"),
            texts=['简体中文', 'English', self.tr('Use system setting')],
            parent=self.customizeGroup
        )

        # Update
        self.updateSoftwareGroup = SettingCardGroup(self.tr("Software Update"), self.scrollWidget)

        self.updateCheckCard = PushSettingCard(
            self.tr("Check"),
            FluentIcon.UPDATE,
            self.tr("Find available updates"),
            "",
            self.updateSoftwareGroup
        )

        self.__initWidget()
        log.infoWrite("[SubWidget][Settings] Initialized")

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 120, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)

        # initialize style sheet
        self.__setQss()

        # initialize layout
        self.initLayout()
        self.__connectSignalToSlot()

    def initLayout(self):
        self.settingLabel.move(60, 63)

        # Storage

        self.storageGroup.addSettingCard(self.storageDataCard)
        self.storageGroup.addSettingCard(self.storageCacheCard)
        self.storageGroup.addSettingCard(self.storageLogCard)
        self.storageGroup.addSettingCard(self.storageConfigCard)

        # Default

        self.defaultGroup.addSettingCard(self.defaultLogDeleteCard)

        # Customize

        self.customizeGroup.addSettingCard(self.customizeLanguageSetting)

        self.updateSoftwareGroup.addSettingCard(self.updateCheckCard)

        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(60, 10, 60, 0)
        self.expandLayout.addWidget(self.storageGroup)
        self.expandLayout.addWidget(self.defaultGroup)
        self.expandLayout.addWidget(self.customizeGroup)
        self.expandLayout.addWidget(self.updateSoftwareGroup)

    def __setQss(self):
        """ set style sheet """
        self.scrollWidget.setObjectName('scrollWidget')
        self.settingLabel.setObjectName('settingLabel')

        theme = 'dark' if isDarkTheme() else 'light'
        with open(f"{utils.workingDir}/assets/themes/{theme}_setting_interface.qss",
                  encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def __showMessageBox(self, title, content):
        Dialog(title, content, self).exec()

    def __defaultLogDeleteCardClicked(self):
        utils.deleteAllLogFiles()
        log.infoWrite("[SubWidget][Settings] All old logs deleted")
        infoBars.successBar(self.tr("Success"), self.tr("All old logs deleted"), parent=self.window())

    def __connectSignalToSlot(self):
        """ connect signal to slot """
        cfg.appRestartSig.connect(lambda: infoBars.warningBar(self.tr("Warning"), self.tr(
            "Please restart the application to apply the changes"), parent=self.window()))

        # Storage
        self.storageDataCard.clicked.connect(lambda: utils.openFolder(cfg.get(cfg.storageDataFolders)))
        self.storageCacheCard.clicked.connect(lambda: utils.openFolder(cfg.get(cfg.storageCacheFolders)))
        self.storageLogCard.clicked.connect(lambda: utils.openFolder(cfg.get(cfg.storageLogFolders)))
        self.storageConfigCard.clicked.connect(lambda: utils.openFolder(self.configPath))

        # Default
        self.defaultLogDeleteCard.clicked.connect(self.__defaultLogDeleteCardClicked)

        # Update
        self.updateCheckCard.clicked.connect(lambda: self.__showMessageBox(self.tr("Oops!"), self.tr("This feature is not available yet!")))