# coding:utf-8
import json

from ..Scripts.UI import customMsgBox, customDialog
from ..Scripts.UI.styleSheet import StyleSheet
from ..Scripts.Utils import ConfigUtils, logTracker as log
from ..Core.UIGF.importSupport import ImportSupport
from ..Core.UIGF.exportSupport import ExportSupport
from qfluentwidgets import (SettingCardGroup, PushSettingCard, ScrollArea,
                            ComboBoxSettingCard, ExpandLayout, isDarkTheme, MessageBox, OptionsSettingCard,
                            SwitchSettingCard, HyperlinkCard)
from qfluentwidgets import FluentIcon
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QLabel, QFileDialog

utils = ConfigUtils.ConfigUtils()


class LinkWidget(ScrollArea):
    checkUpdateSig = Signal()

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)
        self.linkLabel = QLabel("UIGF 导入和导出", self)

        self.configPath = utils.configPath

        # Import
        self.importGroup = SettingCardGroup("导入", self.scrollWidget)
        self.importCard = PushSettingCard(
            "浏览",
            FluentIcon.EMBED,
            "导入 UIGF(Json) 文件",
            "目前支持的标准: Uniformed Interchangeable GachaLog Format standard v2.2",
            self.importGroup
        )

        # Export
        self.exportGroup = SettingCardGroup("导出", self.scrollWidget)
        self.exportCard = PushSettingCard(
            "浏览",
            FluentIcon.SHARE,
            "导出 UIGF(Json) 文件",
            "目前支持的标准: Uniformed Interchangeable GachaLog Format standard v2.2",
            self.exportGroup
        )

        # AboutUIGF
        self.uigfGroup = SettingCardGroup("关于 UIGF", self.scrollWidget)
        self.uigfCard = HyperlinkCard(
            f"https://uigf.org/zh/",
            "打开 UIGF 官网",
            FluentIcon.HELP,
            "什么是UIGF?",
            "Unified Standardized GenshinData Format",
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

        StyleSheet.LINK_FRAME.apply(self)

    def __showMessageBox(self, title, content):
        MessageBox(title, content, self).exec()

    def __showTextEditMessageBox(self, title, content, text):
        customMsgBox.TextEditMsgBox(title, content, text, self).exec()

    def __importCardClicked(self):
        filePath = QFileDialog.getOpenFileName(self, "打开 UIGF(Json) 文件", "./", "UIGF(json) File (*.json)")[0]
        if utils.jsonValidator(filePath, "uigf"):
            log.infoWrite(f"[Sangonomiya][Link] UIGF Import File Path: {filePath}")
            importFile = json.loads(open(filePath, 'r', encoding="utf-8").read())
            tmp_uid = importFile["info"]["uid"]
            tmp_language = importFile["info"]["lang"]
            tmp_export_time = importFile["info"].get("export_time", "Unknown")
            tmp_export_application = importFile["info"]["export_app"]
            tmp_application_version = importFile["info"]["export_app_version"]
            alertMessage = f'''UID: {tmp_uid}
语言: {tmp_language}
导出时间: {tmp_export_time}  
导出应用: {tmp_export_application}
导出应用版本: {tmp_application_version}'''
            self.__showTextEditMessageBox("验证", "请验证如下信息:", alertMessage)
            importSupport = ImportSupport(tmp_uid, tmp_language, tmp_export_time, tmp_export_application, tmp_application_version)
            importSupport.UIGFSave(importFile)

    def __exportCardReturnSignal(self, uid):
        filePath = QFileDialog.getSaveFileName(self, "保存 UIGF(Json) 文件", f"./{uid}_export_data.json", "UIGF(json) File (*.json)")[0]
        exportSupport = ExportSupport(uid)
        exportSupport.UIGFSave(filePath)


    def __exportCardClicked(self):
        w = customDialog.ComboboxDialog("导出", "选择需要导出的UID", self)
        w.returnSignal.connect(self.__exportCardReturnSignal)
        w.exec()


    def __connectSignalToSlot(self):
        self.importCard.clicked.connect(self.__importCardClicked)
        self.exportCard.clicked.connect(self.__exportCardClicked)