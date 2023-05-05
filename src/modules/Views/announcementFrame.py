import webbrowser
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QFrame, QLabel, QHBoxLayout, QListWidget, QVBoxLayout, QSizePolicy
from qfluentwidgets import PrimaryPushButton, FluentIcon, TextEdit, PushButton, StateToolTip, InfoBarPosition

from ..Scripts.UI import infoBars
from ..Scripts.Utils import downloader
from ..Scripts.Utils.ConfigUtils import ConfigUtils
from ..Scripts.Utils import logTracker as log
from .ViewFunctions import announcementFunctions

utils = ConfigUtils()


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
        self.currentAnnounceHTMLPath = ""

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
        self.contentNoBanner = QLabel(self.tr("This announcement has no cover"), self)
        self.contentHTMLBtn = PushButton(self)
        self.contentVBox.addWidget(self.contentBanner)
        self.contentVBox.addStretch(1)
        self.contentVBox.addWidget(self.contentNoBanner)
        self.contentVBox.addStretch(1)
        self.contentVBox.addWidget(self.contentHTMLBtn)
        self.announceHBox.addLayout(self.contentVBox)

        self.baseVBox.addLayout(self.announceHBox)

        self.announceFunc = announcementFunctions.AnnouncementFunctions(self.announceData, self.announceIconData)
        self.initAnnounce()

        self.setObjectName("AnnouncementFrame")

        self.initFrame()

    def initFrame(self):
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
        self.announceListBox.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.announceListBox.currentItemChanged.connect(self.__announceListBoxItemChanged)
        self.announceListBox.setCurrentRow(0)
        # Content
        self.contentBanner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.contentBanner.setMaximumWidth(750)
        self.contentBanner.setScaledContents(True)
        self.contentNoBanner.setFont(utils.getFont(24))
        self.contentNoBanner.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.contentNoBanner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.contentNoBanner.setStyleSheet("color: #FFFFFF;")
        self.contentHTMLBtn.setText(self.tr("Details"))
        self.contentHTMLBtn.setFixedSize(750, 30)
        self.contentHTMLBtn.clicked.connect(self.openAnnounce)
        # Refresh
        self.headerRightRefreshBtn.clicked.connect(self.refreshAnnounce)

    def __announceListBoxItemChanged(self):
        currentAnnounceData = self.announceFunc.getCurrentAnnounce(self.announceListBox.currentIndex().row())
        self.headerLeftContentTitleLabel.setText(currentAnnounceData["bigTitle"])
        self.contentBanner.hide()
        if currentAnnounceData["banner"]:
            self.contentBanner.show()
            self.contentNoBanner.hide()
            self.contentBanner.setPixmap(currentAnnounceData["banner"])
            self.contentBanner.setFixedHeight(currentAnnounceData["bannerHeight"])
        else:
            self.contentNoBanner.show()
        self.currentAnnounceHTMLPath = currentAnnounceData["contentHtml"]

    def initAnnounce(self):
        self.announceFunc.getIcons()
        self.headerRightAnnounceDateLabel.setText(
            self.tr("Updated on ") + utils.getFileDate(f"{utils.workingDir}/cache/announce.json"))
        for index, item in enumerate(self.announceFunc.getItems()):
            self.announceListBox.addItem(item)
            self.announceListBox.item(index).setSizeHint(QSize(300, 30))

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
        self.initAnnounce()
        infoBars.successBar(self.tr("Success"), self.tr("Announcement Updated"), "t", self)

    def openAnnounce(self):
        webbrowser.open(f"{utils.workingDir}/cache/{self.announceListBox.currentRow()}.html")
