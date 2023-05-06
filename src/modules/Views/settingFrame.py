# coding:utf-8
from .ViewConfigs.config import cfg
from ..Core.GachaReport.gachaReportUtils import getDefaultGameDataPath
from ..Scripts.UI import customIcon
from ..Scripts.UI.styleSheet import StyleSheet
from ..Scripts.Utils import ConfigUtils
from ..Scripts.Utils import logTracker as log
from qfluentwidgets import (SettingCardGroup, PushSettingCard, ScrollArea,
                            ComboBoxSettingCard, ExpandLayout, isDarkTheme, Dialog, OptionsSettingCard,
                            SwitchSettingCard, setTheme, Theme, InfoBar)
from qfluentwidgets import FluentIcon, InfoBarPosition, qconfig
from PyQt6 import QtGui
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QLabel, QApplication, QFileDialog

utils = ConfigUtils.ConfigUtils()


class SettingWidget(ScrollArea):
    checkUpdateSig = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)
        self.settingLabel = QLabel(self.tr("Settings"), self)

        self.configPath = utils.configPath

        # Game

        self.gameGroup = SettingCardGroup(self.tr("Game"), self.scrollWidget)
        self.gameDataCard = PushSettingCard(
            self.tr("Browse"),
            FluentIcon.FOLDER,
            self.tr("Game Folder"),
            cfg.get(cfg.gameDataFolder),
            self.gameGroup
        )
        self.gameDataResetCard = PushSettingCard(
            self.tr("Reset"),
            FluentIcon.CLOSE,
            self.tr("Reset the game folder location"),
            self.tr("If you specified the game path incorrectly, reset."),
            self.gameGroup
        )

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

        self.defaultCacheDeleteCard = PushSettingCard(
            self.tr("Delete"),
            customIcon.MyFluentIcon.DELETE,
            f"{self.tr('Delete all cache files')} ({self.tr('About')} {utils.getDirSize(utils.workingDir + '/cache')} MB)",
            f"All cache files in {utils.workingDir + '/cache'} will be deleted",
            self.defaultGroup
        )

        # Customize
        self.customizeGroup = SettingCardGroup(self.tr("Customize"), self.scrollWidget)

        self.customizeThemeSetting = OptionsSettingCard(
            qconfig.themeMode,
            FluentIcon.BRUSH,
            self.tr('Application theme'),
            self.tr("Change the appearance of your application"),
            texts=[
                self.tr('Light'), self.tr('Dark'),
                self.tr('Use system setting')
            ],
            parent=self.customizeGroup
        )

        self.customizeLanguageSetting = ComboBoxSettingCard(
            cfg.customizeLanguage,
            FluentIcon.LANGUAGE,
            self.tr("Language"),
            self.tr("Set the language"),
            texts=['简体中文', 'English', self.tr('Use system setting')],
            parent=self.customizeGroup
        )

        self.customizeAutoDeleteLogSetting = SwitchSettingCard(
            FluentIcon.DELETE,
            self.tr('Automatically delete old logs'),
            self.tr("Delete all previous logs each time the application is started"),
            configItem=cfg.customizeAutoDeleteLog,
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
        self.setObjectName("SettingFrame")
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

        # Game

        self.gameGroup.addSettingCard(self.gameDataCard)
        self.gameGroup.addSettingCard(self.gameDataResetCard)

        # Storage

        self.storageGroup.addSettingCard(self.storageDataCard)
        self.storageGroup.addSettingCard(self.storageCacheCard)
        self.storageGroup.addSettingCard(self.storageLogCard)
        self.storageGroup.addSettingCard(self.storageConfigCard)

        # Default

        self.defaultGroup.addSettingCard(self.defaultLogDeleteCard)
        self.defaultGroup.addSettingCard(self.defaultCacheDeleteCard)

        # Customize

        self.customizeGroup.addSettingCard(self.customizeThemeSetting)
        self.customizeGroup.addSettingCard(self.customizeLanguageSetting)
        self.customizeGroup.addSettingCard(self.customizeAutoDeleteLogSetting)

        # Update

        self.updateSoftwareGroup.addSettingCard(self.updateCheckCard)

        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(60, 10, 60, 0)
        self.expandLayout.addWidget(self.gameGroup)
        self.expandLayout.addWidget(self.storageGroup)
        self.expandLayout.addWidget(self.defaultGroup)
        self.expandLayout.addWidget(self.customizeGroup)
        self.expandLayout.addWidget(self.updateSoftwareGroup)

    def __setQss(self):
        """ set style sheet """
        self.scrollWidget.setObjectName('scrollWidget')
        self.settingLabel.setObjectName('settingLabel')

        StyleSheet.SETTING_FRAME.apply(self)

    def __showMessageBox(self, title, content):
        Dialog(title, content, self).exec()

    def __gameDataCardClicked(self):
        folder = QFileDialog.getExistingDirectory(
            self, self.tr("Choose Genshin Impact folder"), "./")
        if not folder or cfg.get(cfg.gameDataFolder) == folder:
            return

        cfg.set(cfg.gameDataFolder, folder)
        self.gameDataCard.setContent(folder)

    def __gameDataResetCardClicked(self):
        cfg.set(cfg.gameDataFolder, getDefaultGameDataPath())
        self.gameDataCard.setContent(getDefaultGameDataPath())

    def __defaultLogDeleteCardClicked(self):
        utils.deleteAllLogFiles()
        log.infoWrite("[Sangonomiya][Settings] All old logs deleted")
        InfoBar.success(self.tr("Success"), self.tr("All old logs deleted"), InfoBarPosition.TOP_RIGHT, parent=self.window())

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        self.__defaultCacheSizeUpdate()

    def __defaultCacheDeleteCardClicked(self):
        utils.deleteAllCacheFiles()
        log.infoWrite("[Sangonomiya][Settings] All cache files deleted")
        self.__defaultCacheSizeUpdate()
        InfoBar.success(self.tr("Success"), self.tr("All old cache files deleted"),InfoBarPosition.TOP_RIGHT, parent=self.window())

    def __defaultCacheSizeUpdate(self):
        self.defaultCacheDeleteCard.titleLabel.setText(f"{self.tr('Delete all cache files')} ({self.tr('About')} {utils.getDirSize(utils.workingDir + '/cache')} MB)")

    def __connectSignalToSlot(self):
        """ connect signal to slot """
        cfg.appRestartSig.connect(lambda: InfoBar.warning(self.tr("Warning"), self.tr(
            "Please restart the application to apply the changes"), parent=self.window(), position=InfoBarPosition.TOP_RIGHT))
        cfg.themeChanged.connect(setTheme)

        # Game
        self.gameDataCard.clicked.connect(self.__gameDataCardClicked)
        self.gameDataResetCard.clicked.connect(self.__gameDataResetCardClicked)

        # Storage
        self.storageDataCard.clicked.connect(lambda: utils.openFolder(cfg.get(cfg.storageDataFolders)))
        self.storageCacheCard.clicked.connect(lambda: utils.openFolder(cfg.get(cfg.storageCacheFolders)))
        self.storageLogCard.clicked.connect(lambda: utils.openFolder(cfg.get(cfg.storageLogFolders)))
        self.storageConfigCard.clicked.connect(lambda: utils.openFolder(self.configPath))

        # Default
        self.defaultLogDeleteCard.clicked.connect(self.__defaultLogDeleteCardClicked)
        self.defaultCacheDeleteCard.clicked.connect(self.__defaultCacheDeleteCardClicked)

        # Update
        self.updateCheckCard.clicked.connect(lambda: self.__showMessageBox(self.tr("Oops!"), self.tr("This feature is not available yet!")))