import json
import sys

from PyQt6 import QtGui

sys.path.append("..")

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QFrame, QLabel, QHBoxLayout, QPushButton, QListWidget, QVBoxLayout
from qfluentwidgets import PrimaryPushButton, FluentIcon, StateToolTip, TextEdit

from components import OSUtils, downloader
from modules.subWidgetFunctions import announcementFunctions

utils = OSUtils.OSUtils()


class AnnouncementWidget(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        downloader.downloadFromJson(utils.getAnnounceRequestURL(), utils.workingDir + "/cache/", "announce.json")
        downloader.downloadFromJson(utils.getAnnounceIconRequestURL(), utils.workingDir + "/cache/",
                                    "announce_icons.json")

        self.baseVBox = QVBoxLayout(self)

        self.announceData = utils.getAnnounceData()
        self.announceIconData = utils.getAnnounceIconData()
        self.isAnnounceDataAvailable = False if (self.announceData is None) or (self.announceIconData is None) else True

        if self.isAnnounceDataAvailable:
            self.baseAnnounceTitleLabel = QLabel(self)
            self.baseContentTitleLabel = QLabel(self)
            self.baseVBox.addWidget(self.baseAnnounceTitleLabel)
            self.baseVBox.addWidget(self.baseContentTitleLabel)

            self.announceHBox = QHBoxLayout(self)

            self.announceListBox = QListWidget(self)
            self.announceHBox.addWidget(self.announceListBox)

            self.contentVBox = QVBoxLayout(self)
            self.contentBanner = QLabel(self)
            self.content = TextEdit(self)
            self.contentVBox.addWidget(self.contentBanner)
            self.contentVBox.addWidget(self.content)
            self.announceHBox.addLayout(self.contentVBox)

            self.baseVBox.addLayout(self.announceHBox)

            self.announceFunc = announcementFunctions.AnnouncementFunctions(self.announceData, self.announceIconData)
            self.initAnnounce()
        else:
            self.unBaseAnnounceTitleLabel = QLabel(self.tr("Unable to connect to the Internet"), self)
            self.unBaseContentTitleLabel = QLabel(
                self.tr("You may need to check whether your Internet access is available."), self)
            self.unRetryBtn = PrimaryPushButton(self.tr("Retry"), self, FluentIcon.UPDATE)

            self.baseVBox.addStretch(1)
            self.baseVBox.addWidget(self.unBaseAnnounceTitleLabel)
            self.baseVBox.addWidget(self.unBaseContentTitleLabel)
            self.baseVBox.addSpacing(15)
            self.baseVBox.addWidget(self.unRetryBtn, 0, Qt.AlignmentFlag.AlignCenter)
            self.baseVBox.addStretch(1)

        self.setObjectName("AnnouncementWidget")

        self.initFrame()

    def initFrame(self):
        if self.isAnnounceDataAvailable:
            # Top
            self.baseAnnounceTitleLabel.setText(self.tr("Announcement"))
            self.baseAnnounceTitleLabel.setFont(utils.getFont(18))
            self.baseAnnounceTitleLabel.setStyleSheet("color: #FFFFFF;")
            self.baseContentTitleLabel.setText(self.tr("Have not selected any announcement"))
            self.baseContentTitleLabel.setFont(utils.getFont(10))
            self.baseContentTitleLabel.setStyleSheet("color: grey;")
            # List
            self.announceListBox.setFixedWidth(300)
            self.announceListBox.setFrameShape(QFrame.Shape.NoFrame)
            self.announceListBox.setStyleSheet("background-color: #272727; color: #FFFFFF;")
            self.contentBanner.setScaledContents(True)
            # Content
            self.contentBanner.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.contentBanner.setMaximumWidth(750)
            self.content.setReadOnly(True)
            #self.content.setMaximumWidth(750)
        else:
            # Unavailable
            self.unBaseAnnounceTitleLabel.setFont(utils.getFont(32))
            self.unBaseAnnounceTitleLabel.setStyleSheet("color: #FFFFFF;")
            self.unBaseAnnounceTitleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.unBaseContentTitleLabel.setFont(utils.getFont(16))
            self.unBaseContentTitleLabel.setStyleSheet("color: grey;")
            self.unBaseContentTitleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.unRetryBtn.setFixedWidth(100)

    def __announceListBoxItemChanged(self):
        currentAnnounceData = self.announceFunc.getCurrentAnnounce(self.announceListBox.currentIndex().row())
        self.baseContentTitleLabel.setText(currentAnnounceData["bigTitle"])
        self.contentBanner.setPixmap(currentAnnounceData["banner"])
        self.contentBanner.setFixedHeight(currentAnnounceData["bannerHeight"])
        self.content.setHtml(currentAnnounceData["contentHtml"])

    def initAnnounce(self):
        self.announceFunc.getIcons()
        for index, item in enumerate(self.announceFunc.getItems()):
            self.announceListBox.addItem(item)
            self.announceListBox.item(index).setSizeHint(QSize(300, 30))
        self.announceListBox.currentItemChanged.connect(self.__announceListBoxItemChanged)
