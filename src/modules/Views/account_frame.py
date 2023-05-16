import asyncio

from PySide6.QtGui import QPixmap
from PySide6 import QtGui, QtWidgets
from PySide6.QtWidgets import QFrame, QLabel, QHBoxLayout, QVBoxLayout

from qfluentwidgets import HyperlinkCard, isDarkTheme, TextEdit, ComboBox
from qfluentwidgets import FluentIcon

from .ViewFunctions.accountFunctions import AccountGetInfoThread
from ..Core.GachaReport import gacha_report_read
from .ViewConfigs.config import cfg
from ..Scripts.UI.style_sheet import StyleSheet
from ..Scripts.Utils import config_utils, log_recorder as log

utils = config_utils.ConfigUtils()


class AccountWidget(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.currentUID = ""

        self.baseVBox = QVBoxLayout(self)

        self.headerHBox = QHBoxLayout(self)
        self.headerLeftTitleLabel = QLabel("个人信息", self)
        self.headerRightUIDComboBox = ComboBox()
        self.headerHBox.addWidget(self.headerLeftTitleLabel)
        self.headerHBox.addWidget(self.headerRightUIDComboBox)

        self.basicHBox = QHBoxLayout(self)
        self.basicAvatarLabel = QLabel(self)
        self.basicVBox = QVBoxLayout(self)
        self.basicNameLabel = QLabel("未知", self)
        self.basicSignatureLabel = QLabel("未知", self)
        self.basicVBox.addWidget(self.basicNameLabel)
        self.basicVBox.addWidget(self.basicSignatureLabel)
        self.basicHBox.addWidget(self.basicAvatarLabel)
        self.basicHBox.addLayout(self.basicVBox)

        self.detailTitleLabel = QLabel("详细信息", self)
        self.detailTextEdit = TextEdit()

        self.baseVBox.addLayout(self.headerHBox)
        self.baseVBox.addLayout(self.basicHBox)
        self.baseVBox.addWidget(self.detailTitleLabel)
        self.baseVBox.addWidget(self.detailTextEdit)

        self.setObjectName("AccountFrame")
        self.initFrame()
        StyleSheet.ACCOUNT_FRAME.apply(self)
        log.infoWrite("[Account] UI initialized")

    def initFrame(self):
        self.headerLeftTitleLabel.setObjectName("headerLeftTitleLabel")
        self.headerRightUIDComboBox.setFixedWidth(160)

        self.basicAvatarLabel.setFixedSize(79, 64)
        self.basicAvatarLabel.setScaledContents(True)
        self.basicAvatarLabel.setObjectName("basicAvatarLabel")
        self.basicNameLabel.setObjectName("basicNameLabel")
        self.basicSignatureLabel.setObjectName("basicSignatureLabel")

        self.detailTitleLabel.setObjectName("detailTitleLabel")
        self.detailTextEdit.setReadOnly(True)
        self.detailTextEdit.setFont(utils.getFont(14))

    def __accountGetInfoSignal(self, result):
        if result["icon_url"] == "正在获取...":
            self.basicAvatarLabel.setPixmap(QPixmap(f"{utils.workingDir}/assets/unknownAvatar.png"))
        else:
            self.basicAvatarLabel.setPixmap(QPixmap(f"{utils.workingDir}/cache/{result['icon_url'].split('/')[-1]}"))
        self.basicNameLabel.setText(f"{result['nickname']} ({result['level']})")
        self.basicSignatureLabel.setText(result["signature"])
        text = f'''成就数: {result['achievement']}
深渊层数: {result['abyss_floor']}
        '''
        self.detailTextEdit.setText(text)

    def __headerRightUIDComboBoxChanged(self):
        self.accountGetInfoThread = AccountGetInfoThread(self.headerRightUIDComboBox.currentText())
        self.accountGetInfoThread.start()
        self.accountGetInfoThread.trigger.connect(self.__accountGetInfoSignal)
        log.infoWrite("[Account] Basic Info Get")

    def showEvent(self, event):
        self.headerRightUIDComboBox.clear()
        self.headerRightUIDComboBox.addItems(gacha_report_read.getUIDList())
        self.currentUID = cfg.gachaReportLastUID.value
        if self.currentUID:
            self.headerRightUIDComboBox.setCurrentText(self.currentUID)
            self.__headerRightUIDComboBoxChanged()
        else:
            self.headerRightUIDComboBox.setCurrentIndex(0)
            self.__headerRightUIDComboBoxChanged()


