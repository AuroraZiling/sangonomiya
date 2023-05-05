# coding:utf-8
import json
from ..Scripts.UI import customMsgBox
from ..Scripts.Utils import ConfigUtils
from qfluentwidgets import (SettingCardGroup, PushSettingCard, ScrollArea,
                            ComboBoxSettingCard, ExpandLayout, isDarkTheme, MessageBox, OptionsSettingCard,
                            SwitchSettingCard, HyperlinkCard)
from qfluentwidgets import FluentIcon
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QLabel, QFileDialog

utils = ConfigUtils.ConfigUtils()


class LinkWidget(ScrollArea):
    checkUpdateSig = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)
        self.linkLabel = QLabel(self.tr("UIGF Import & Export"), self)

        self.configPath = utils.configPath

        # Import
        self.importGroup = SettingCardGroup(self.tr("Import"), self.scrollWidget)
        self.importCard = PushSettingCard(
            self.tr("Browse"),
            FluentIcon.EMBED,
            self.tr("Import UIGF(Json) File"),
            self.tr("Currently supported standards: Uniformed Interchangeable GachaLog Format standard v2.2"),
            self.importGroup
        )

        # Export
        self.exportGroup = SettingCardGroup(self.tr("Export"), self.scrollWidget)
        self.exportCard = PushSettingCard(
            self.tr("Browse"),
            FluentIcon.SHARE,
            self.tr("Export UIGF(Json) File"),
            self.tr("Currently supported standards: Uniformed Interchangeable GachaLog Format standard v2.2"),
            self.exportGroup
        )

        # AboutUIGF
        self.uigfGroup = SettingCardGroup(self.tr("About UIGF"), self.scrollWidget)
        self.uigfCard = HyperlinkCard(
            f"https://uigf.org/{self.tr('en')}/",
            self.tr("Open UIGF Official WebSite"),
            FluentIcon.HELP,
            self.tr('What is UIGF?'),
            self.tr("Unified Standardized GenshinData Format"),
            self.uigfGroup
        )

        self.setObjectName("LinkFrame")
        self.__initWidget()

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
        self.linkLabel.move(60, 63)

        # Import
        self.importGroup.addSettingCard(self.importCard)

        # Export
        self.exportGroup.addSettingCard(self.exportCard)

        # About UIGF
        self.uigfGroup.addSettingCard(self.uigfCard)

        # Add Cards
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(60, 10, 60, 0)
        self.expandLayout.addWidget(self.importGroup)
        self.expandLayout.addWidget(self.exportGroup)
        self.expandLayout.addWidget(self.uigfGroup)

    def __setQss(self):
        """ set style sheet """
        self.scrollWidget.setObjectName('scrollWidget')
        self.linkLabel.setObjectName('linkLabel')

        theme = 'dark' if isDarkTheme() else 'light'
        with open(f"{utils.workingDir}/assets/themes/{theme}_link_interface.qss",
                  encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def __showMessageBox(self, title, content):
        MessageBox(title, content, self).exec()

    def __showTextEditMessageBox(self, title, content, text):
        customMsgBox.TextEditMsgBox(title, content, text, self).exec()

    def __importCardClicked(self):
        filePath = QFileDialog.getOpenFileName(self, self.tr("Open UIGF(json) file"), "./", "UIGF(json) File (*.json)")[0]
        if utils.jsonValidator(filePath, "uigf"):
            importFile = json.loads(open(filePath, 'r', encoding="utf-8").read())
            alertMessage = f'''UID: {importFile["info"]["uid"]}
{self.tr("Language")}: {importFile["info"]["lang"]}
{self.tr("Export Time")}: {importFile["info"]["export_time"]}  
{self.tr("Export Application")}: {importFile["info"]["export_app"]}
{self.tr("Export Application Version")}: {importFile["info"]["export_app_version"]}'''

            self.__showTextEditMessageBox(self.tr("Verify"), self.tr("Please verify the following information:"), alertMessage)

    def __connectSignalToSlot(self):
        self.importCard.clicked.connect(self.__importCardClicked)