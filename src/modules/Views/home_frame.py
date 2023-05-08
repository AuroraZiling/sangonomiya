from PySide6.QtWidgets import QFrame, QLabel, QHBoxLayout, QVBoxLayout

from qfluentwidgets import PrimaryPushButton, FluentIcon, TextEdit

from ..Scripts.UI.style_sheet import StyleSheet
from ..Scripts.Utils import config_utils, log_recorder as log

utils = config_utils.ConfigUtils()


class HomeWidget(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.baseVBox = QVBoxLayout(self)

        self.topHBox = QHBoxLayout(self)

        self.topTitleLabel = QLabel("Sangonomiya", self)
        self.topRefreshBtn = PrimaryPushButton("刷新", self, FluentIcon.SYNC)

        self.topHBox.addWidget(self.topTitleLabel)
        self.topHBox.addWidget(self.topRefreshBtn)
        self.baseVBox.addLayout(self.topHBox)

        self.announceTitleLabel = QLabel("公告", self)
        self.announceTextBox = TextEdit(self)

        self.baseVBox.addWidget(self.announceTitleLabel)
        self.baseVBox.addWidget(self.announceTextBox)

        self.setObjectName("HomeFrame")
        StyleSheet.HOME_FRAME.apply(self)

        self.initFrame()
        self.getAnnouncementFromMetaData()

        log.infoWrite("[Home] UI Initialized")

    def initFrame(self):
        self.topTitleLabel.setObjectName("homeFrameTitle")
        self.topRefreshBtn.setFixedWidth(100)

        self.announceTitleLabel.setObjectName("homeFrameAnnounceTitle")
        self.announceTextBox.setObjectName("homeFrameAnnounce")
        self.announceTextBox.setReadOnly(True)
        self.announceTextBox.setFrameShape(QFrame.Shape.NoFrame)
        self.announceTextBox.setContentsMargins(5, 5, 5, 5)

    def getAnnouncementFromMetaData(self):
        content = f'''Sangonomiya Version is {utils.appVersion}
PyQt-fluent-widgets Version is {utils.UIVersion}
Sangonomiya is working at {utils.workingDir}'''
        self.announceTextBox.setText(content)
        log.infoWrite("[Home] Announcement Set")
