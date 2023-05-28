# coding:utf-8
import json
import logging

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QLabel, QFileDialog

from qfluentwidgets import SettingCardGroup, PushSettingCard, ScrollArea, ExpandLayout, MessageBox, HyperlinkCard, \
    InfoBar, InfoBarPosition
from qfluentwidgets import FluentIcon

from ..Core.GachaReport import gacha_report_read
from ..Scripts.UI import custom_msgBox, custom_dialog
from ..Scripts.UI.style_sheet import StyleSheet
from ..Scripts.Utils import tools
from ..Core.UIGF.import_support import ImportSupport
from ..Core.UIGF.export_support import ExportSupport

utils = tools.Tools()


class LinkWidget(ScrollArea):
    checkUpdateSig = Signal()

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)
        self.linkLabel = QLabel("UIGF 导入和导出", self)

        self.uigfStandard = "UIGF(Json) v2.2"

        # Import
        self.importGroup = SettingCardGroup("导入", self.scrollWidget)
        self.importCard = PushSettingCard(
            "浏览",
            FluentIcon.EMBED,
            "导入 UIGF(Json) 文件",
            "目前支持的标准: 统一可交换抽卡记录标准 v2.2 和 v2.3",
            self.importGroup
        )

        # Export
        self.exportGroup = SettingCardGroup("导出", self.scrollWidget)
        self.exportCard = PushSettingCard(
            "浏览",
            FluentIcon.SHARE,
            "导出 UIGF(Json) 文件",
            "目前支持的标准: 统一可交换抽卡记录标准 v2.2 和 v2.3",
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

        logging.info(f"[Link] UI Initialized")

    def __initWidget(self):
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

    def __importCardClicked(self):
        filePath = QFileDialog.getOpenFileName(self, "打开 UIGF(Json) 文件", "./", "UIGF(json) File (*.json)")[0]
        logging.info(f"[Link][Import] Get UIGF File: {filePath}")
        if utils.json_validator(filePath, "uigf"):
            logging.info(f"[Sangonomiya][Link] UIGF Import File Path: {filePath}")
            importFile = json.loads(open(filePath, 'r', encoding="utf-8").read())
            tmp_uid = importFile["info"]["uid"]
            tmp_language = importFile["info"]["lang"]
            tmp_export_time = importFile["info"].get("export_time", "Unknown")
            tmp_export_application = importFile["info"]["export_app"]
            tmp_application_version = importFile["info"]["export_app_version"]
            tmp_uigf_version = importFile["info"]["uigf_version"]
            if tmp_uigf_version == "v2.2" or (tmp_uigf_version == "v2.3" and utils.json_validator(filePath, "v2.3")):
                alertMessage = f'''UID: {tmp_uid}
语言: {tmp_language}
导出时间: {tmp_export_time}  
导出应用: {tmp_export_application}
导出应用版本: {tmp_application_version}
UIGF(Json)版本: {tmp_uigf_version}'''
                w = custom_msgBox.TextEditMsgBox("验证", "请验证如下信息:", alertMessage, self)
                if w.exec():
                    importSupport = ImportSupport(tmp_uid, tmp_language, tmp_export_time)
                    importSupport.UIGFSave(importFile)
                    InfoBar.success("成功", f"档案 {tmp_uid} 已成功导入", InfoBarPosition.TOP_RIGHT, parent=self.window())

                    logging.info(f"[Link][Import] Imported ({tmp_uid} from {tmp_export_application})")
        else:
            InfoBar.error("导入失败", "导入的文件不是有效的UIGF文件", InfoBarPosition.TOP_RIGHT, parent=self)

    def __exportCardReturnSignal(self, uid):
        filePath = QFileDialog.getSaveFileName(self, "保存 UIGF(Json) 文件", f"./{uid}_export_data.json",
                                               "UIGF(json) File (*.json)")[0]
        if filePath:
            exportSupport = ExportSupport(uid, self.uigfStandard)
            exportSupport.UIGFSave(filePath)
            InfoBar.success("成功", f"档案 {uid} 已成功导出", InfoBarPosition.TOP_RIGHT, parent=self.window())
            logging.info(f"[Link][Export] Exported ({uid} to {filePath})")

    def __exportCardStandardReturnSignal(self, choice):
        self.uigfStandard = choice
        if choice == "UIGF(Json) v2.3" and not utils.read_metadata("uigf_dict"):
            self.uigfStandard = "unavailable"
            InfoBar.error("失败", "UIGF API - Dict 不存在，请更新UIGF API元数据", InfoBarPosition.TOP_RIGHT,
                          parent=self.window())
            logging.error(f"[Link][Export] Export Failed. Possible Reason: configs/metadata/uigf_dict.json not found")

    def __exportCardClicked(self):
        w = custom_dialog.ComboboxDialog("导出", "选择UIGF导出标准", ["UIGF(Json) v2.2", "UIGF(Json) v2.3"], self)
        w.returnSignal.connect(self.__exportCardStandardReturnSignal)
        if w.exec() and not self.uigfStandard == "unavailable":
            w = custom_dialog.ComboboxDialog("导出", "选择需要导出的UID", gacha_report_read.getUIDList(), self)
            w.returnSignal.connect(self.__exportCardReturnSignal)
            w.exec()

    def __connectSignalToSlot(self):
        self.importCard.clicked.connect(self.__importCardClicked)
        self.exportCard.clicked.connect(self.__exportCardClicked)
