import os.path
import sys

sys.path.append("..")

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QFrame, QLabel, QHBoxLayout, QListWidget, QVBoxLayout
from qfluentwidgets import PrimaryPushButton, FluentIcon, TextEdit

from components import OSUtils, downloader
from components import logTracker as log
from modules.subWidgetFunctions import announcementFunctions

utils = OSUtils.OSUtils()


class AnnouncementWidget(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        if not (utils.jsonValidator(f"{utils.workingDir}/cache/announce.json") and utils.jsonValidator(f"{utils.workingDir}/cache/announce_icons.json")):
            log.infoWrite("[SubWidget][Announcement] Get announce.json")
            downloader.downloadFromJson(utils.getAnnounceRequestURL(), utils.workingDir + "/cache/", "announce.json")
            log.infoWrite("[SubWidget][Announcement] Get announce_icon.json")
            downloader.downloadFromJson(utils.getAnnounceIconRequestURL(), utils.workingDir + "/cache/",
                                        "announce_icons.json")

        self.baseVBox = QVBoxLayout(self)

        self.announceData = utils.getAnnounceData()
        self.announceIconData = utils.getAnnounceIconData()
        self.isAnnounceDataAvailable = False if (self.announceData is None) or (self.announceIconData is None) else True

        if self.isAnnounceDataAvailable:
            self.headerHBox = QHBoxLayout(self)

            self.headerLeftVBox = QVBoxLayout(self)
            self.headerLeftAnnounceTitleLabel = QLabel(self)
            self.headerLeftContentTitleLabel = QLabel(self)
            self.headerLeftVBox.addWidget(self.headerLeftAnnounceTitleLabel)
            self.headerLeftVBox.addWidget(self.headerLeftContentTitleLabel)

            self.headerHBox.addLayout(self.headerLeftVBox)
            self.headerHBox.addStretch(1)

            self.headerRightVBox = QVBoxLayout(self)
            self.headerRightRefreshBtn = PrimaryPushButton(self.tr("Refresh"), self, FluentIcon.SYNC)
            self.headerRightAnnounceDateLabel = QLabel(self)
            self.headerRightVBox.addSpacing(3)
            self.headerRightVBox.addWidget(self.headerRightRefreshBtn, 0, Qt.AlignmentFlag.AlignRight)
            self.headerRightVBox.addWidget(self.headerRightAnnounceDateLabel, 0, Qt.AlignmentFlag.AlignRight)

            self.headerHBox.addLayout(self.headerRightVBox)
            self.headerHBox.addSpacing(5)
            self.baseVBox.addLayout(self.headerHBox)

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
            self.unRetryBtn = (self.tr("Retry"), self, FluentIcon.UPDATE)

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
            # Top - Left
            self.headerLeftAnnounceTitleLabel.setText(self.tr("Announcement"))
            self.headerLeftAnnounceTitleLabel.setFont(utils.getFont(18))
            self.headerLeftAnnounceTitleLabel.setStyleSheet("color: #FFFFFF;")
            self.headerLeftContentTitleLabel.setText(self.tr("Have not selected any announcement"))
            self.headerLeftContentTitleLabel.setFont(utils.getFont(10))
            self.headerLeftContentTitleLabel.setStyleSheet("color: grey;")
            # Top - Right
            self.headerRightRefreshBtn.setFixedWidth(100)
            self.headerRightAnnounceDateLabel.setText(self.tr("Updated on ") + utils.getFileDate(f"{utils.workingDir}/cache/announce.json"))
            self.headerRightAnnounceDateLabel.setStyleSheet("color: #FFFFFF;")
            self.headerRightAnnounceDateLabel.setFont(utils.getFont(10))
            # List
            self.announceListBox.resize(200, 200)
            self.announceListBox.setFrameShape(QFrame.Shape.NoFrame)
            self.announceListBox.setStyleSheet("background-color: #272727; color: #FFFFFF;")
            self.announceListBox.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.contentBanner.setScaledContents(True)
            # Content
            self.contentBanner.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.contentBanner.setMaximumWidth(750)
            self.content.setReadOnly(True)
            # Refresh
            self.headerRightRefreshBtn.clicked.connect(self.refreshAnnounce)
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
        self.headerLeftContentTitleLabel.setText(currentAnnounceData["bigTitle"])
        self.contentBanner.hide()
        if currentAnnounceData["banner"]:
            self.contentBanner.show()
            self.contentBanner.setPixmap(currentAnnounceData["banner"])
            self.contentBanner.setFixedHeight(currentAnnounceData["bannerHeight"])
        self.content.setHtml(currentAnnounceData["contentHtml"])

    def initAnnounce(self):
        self.announceFunc.getIcons()
        self.headerRightAnnounceDateLabel.setText(
            self.tr("Updated on ") + utils.getFileDate(f"{utils.workingDir}/cache/announce.json"))
        for index, item in enumerate(self.announceFunc.getItems()):
            self.announceListBox.addItem(item)
            self.announceListBox.item(index).setSizeHint(QSize(300, 30))
        self.announceListBox.currentItemChanged.connect(self.__announceListBoxItemChanged)
        self.announceListBox.setCurrentRow(0)
        self.__announceListBoxItemChanged()

    def refreshAnnounce(self):
        self.announceListBox.clear()
        log.infoWrite("[SubWidget][Announcement] Get announce.json")
        downloader.downloadFromJson(utils.getAnnounceRequestURL(), utils.workingDir + "/cache/", "announce.json")
        log.infoWrite("[SubWidget][Announcement] Get announce_icon.json")
        downloader.downloadFromJson(utils.getAnnounceIconRequestURL(), utils.workingDir + "/cache/",
                                    "announce_icons.json")
        self.announceData = utils.getAnnounceData()
        self.announceIconData = utils.getAnnounceIconData()
        self.isAnnounceDataAvailable = False if (self.announceData is None) or (self.announceIconData is None) else True
        self.initAnnounce()

