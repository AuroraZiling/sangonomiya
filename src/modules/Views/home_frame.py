from PySide6.QtWidgets import QFrame, QLabel, QHBoxLayout, QVBoxLayout

from qfluentwidgets import PrimaryPushButton, FluentIcon, TextEdit, InfoBar, InfoBarPosition

from .ViewFunctions.homeFunctions import HomeSoftwareAnnouncementThread, HomeCurrentUPThread
from ..Scripts.UI.style_sheet import StyleSheet
from ..Scripts.Utils import config_utils, log_recorder as log

utils = config_utils.ConfigUtils()


class HomeWidget(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.homeCurrentUPThread = None
        self.homeSoftwareAnnouncementThread = None

        self.baseVBox = QVBoxLayout(self)

        self.topHBox = QHBoxLayout(self)

        self.topTitleLabel = QLabel("Sangonomiya", self)
        self.topRefreshBtn = PrimaryPushButton("刷新", self, FluentIcon.SYNC)

        self.topHBox.addWidget(self.topTitleLabel)
        self.topHBox.addWidget(self.topRefreshBtn)
        self.baseVBox.addLayout(self.topHBox)

        self.currentUPTitleLabel = QLabel("当期UP信息", self)
        self.currentUPCharacterLabel = QLabel("暂无", self)
        self.currentUPWeaponLabel = QLabel("暂无", self)

        self.baseVBox.addWidget(self.currentUPTitleLabel)
        self.baseVBox.addWidget(self.currentUPCharacterLabel)
        self.baseVBox.addWidget(self.currentUPWeaponLabel)

        self.announceTitleLabel = QLabel("公告", self)
        self.announceTextBox = TextEdit(self)

        self.baseVBox.addWidget(self.announceTitleLabel)
        self.baseVBox.addWidget(self.announceTextBox)

        self.setObjectName("HomeFrame")
        StyleSheet.HOME_FRAME.apply(self)

        self.initFrame()
        self.getCurrentUPFromMetaData()
        self.getAnnouncementFromMetaData()

        log.infoWrite("[Home] UI Initialized")

    def __topRefreshBtnClicked(self):
        self.getAnnouncementFromMetaData()
        self.getCurrentUPFromMetaData()

    def initFrame(self):
        self.topTitleLabel.setObjectName("homeFrameTitle")
        self.topRefreshBtn.setFixedWidth(100)
        self.topRefreshBtn.clicked.connect(self.__topRefreshBtnClicked)

        self.currentUPTitleLabel.setObjectName("currentUPTitleLabel")
        self.currentUPCharacterLabel.setObjectName("currentUPCharacterLabel")
        self.currentUPWeaponLabel.setObjectName("currentUPWeaponLabel")

        self.announceTitleLabel.setObjectName("homeFrameAnnounceTitle")
        self.announceTextBox.setObjectName("homeFrameAnnounce")
        self.announceTextBox.setReadOnly(True)
        self.announceTextBox.setFrameShape(QFrame.Shape.NoFrame)
        self.announceTextBox.setContentsMargins(5, 5, 5, 5)

    def __getCurrentUPFromMetaDataSignal(self, upType, info):
        if upType == 0:
            self.currentUPCharacterLabel.setText(info)
        elif upType == 1:
            self.currentUPWeaponLabel.setText(info)

    def getCurrentUPFromMetaData(self):
        self.homeCurrentUPThread = HomeCurrentUPThread()
        self.homeCurrentUPThread.start()
        self.homeCurrentUPThread.trigger.connect(self.__getCurrentUPFromMetaDataSignal)
        log.infoWrite("[Home] Current UP Get")

    def __getAnnouncementFromMetaDataSignal(self, info):
        self.announceTextBox.setText(info)

    def getAnnouncementFromMetaData(self):
        self.homeSoftwareAnnouncementThread = HomeSoftwareAnnouncementThread()
        self.homeSoftwareAnnouncementThread.start()
        self.homeSoftwareAnnouncementThread.trigger.connect(self.__getAnnouncementFromMetaDataSignal)
        log.infoWrite("[Home] Announcement Get")
