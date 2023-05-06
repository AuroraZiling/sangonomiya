import asyncio

import requests
from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QFrame, QLabel, QHBoxLayout, QListWidget, QVBoxLayout, QSizePolicy
from qfluentwidgets import PrimaryPushButton, FluentIcon, TextEdit, PushButton, StateToolTip, InfoBarPosition, \
    isDarkTheme, InfoBar, InfoBarIcon

from ..Scripts.Utils.SoftwareAnnouncement import getAnnouncement
from ..Scripts.UI.styleSheet import StyleSheet
from ..Scripts.Utils.ConfigUtils import ConfigUtils

utils = ConfigUtils()


class HomeWidget(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.baseVBox = QVBoxLayout(self)

        self.topHBox = QHBoxLayout(self)

        self.topTitleLabel = QLabel(self.tr("Sangonomiya"), self)
        self.topRefreshBtn = PrimaryPushButton(self.tr("Refresh"), self, FluentIcon.SYNC)

        self.topHBox.addWidget(self.topTitleLabel)
        self.topHBox.addWidget(self.topRefreshBtn)
        self.baseVBox.addLayout(self.topHBox)

        self.announceTitleLabel = QLabel(self.tr("Announcement"), self)
        self.announceTextBox = TextEdit(self)

        self.baseVBox.addWidget(self.announceTitleLabel)
        self.baseVBox.addWidget(self.announceTextBox)

        self.setObjectName("HomeFrame")
        StyleSheet.HOME_FRAME.apply(self)

        self.initFrame()
        self.getAnnouncementFromMetaData()

    def initFrame(self):
        self.topTitleLabel.setObjectName("homeFrameTitle")
        self.topRefreshBtn.setFixedWidth(100)

        self.announceTitleLabel.setObjectName("homeFrameAnnounceTitle")
        self.announceTextBox.setObjectName("homeFrameAnnounce")
        self.announceTextBox.setReadOnly(True)
        self.announceTextBox.setFrameShape(QFrame.Shape.NoFrame)

    def getAnnouncementFromMetaData(self):
        content = f'''Sangonomiya Version is {utils.appVersion}
PyQt-fluent-widgets Version is {utils.UIVersion}
Sangonomiya is working at {utils.workingDir}'''
        self.announceTextBox.setText(content)