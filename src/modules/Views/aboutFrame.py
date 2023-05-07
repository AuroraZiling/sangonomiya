from PySide6 import QtGui, QtWidgets
from PySide6.QtWidgets import QFrame, QLabel, QHBoxLayout, QVBoxLayout

from qfluentwidgets import HyperlinkCard, isDarkTheme, TextEdit
from qfluentwidgets import FluentIcon

from ..Scripts.UI import customIcon
from ..Scripts.UI.styleSheet import StyleSheet
from ..Scripts.Utils import ConfigUtils
from ..Scripts.Utils import logTracker as log

utils = ConfigUtils.ConfigUtils()


class AboutWidget(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.aboutVBox = QVBoxLayout(self)

        self.aboutTopHBox = QHBoxLayout(self)

        self.aboutTopProjImage = QLabel("", self)
        self.aboutTopHBox.addWidget(self.aboutTopProjImage)

        self.aboutTopProjDesVBox = QVBoxLayout(self)
        self.aboutTopProjDesLabel = QLabel("Sangonomiya", self)
        self.aboutTopProjDesVersion = QLabel(f"{utils.appVersion} for {utils.OSName}", self)
        self.aboutTopProjDesLicense = QLabel("GPL v3.0", self)
        self.aboutTopProjDesGithub = QLabel("https://github.com/AuroraZiling/sangonomiya", self)
        self.aboutTopProjDesVBox.addWidget(self.aboutTopProjDesLabel)
        self.aboutTopProjDesVBox.addWidget(self.aboutTopProjDesVersion)
        self.aboutTopProjDesVBox.addWidget(self.aboutTopProjDesLicense)
        self.aboutTopProjDesVBox.addWidget(self.aboutTopProjDesGithub)
        self.aboutTopProjDesVBox.addStretch(1)
        self.aboutTopHBox.addLayout(self.aboutTopProjDesVBox)

        self.aboutTopUIImage = QLabel("", self)
        self.aboutTopHBox.addWidget(self.aboutTopUIImage)

        self.aboutTopUIDesVBox = QVBoxLayout(self)
        self.aboutTopUIDesDesignLabel = QLabel("UI Design", self)
        self.aboutTopUIDesLabel = QLabel("PyQt-Fluent-Widgets", self)
        self.aboutTopUIDesVersion = QLabel(f"{utils.UIVersion} for PySide6", self)
        self.aboutTopUIDesGithub = QLabel("https://github.com/zhiyiYo/PyQt-Fluent-Widgets", self)
        self.aboutTopUIDesVBox.addWidget(self.aboutTopUIDesDesignLabel)
        self.aboutTopUIDesVBox.addWidget(self.aboutTopUIDesLabel)
        self.aboutTopUIDesVBox.addWidget(self.aboutTopUIDesVersion)
        self.aboutTopUIDesVBox.addWidget(self.aboutTopUIDesGithub)
        self.aboutTopUIDesVBox.addStretch(1)

        self.aboutTopHBox.addLayout(self.aboutTopUIDesVBox)
        self.aboutVBox.addLayout(self.aboutTopHBox)

        self.aboutOpenSourceVBox = QVBoxLayout(self)
        self.aboutOpenSourceLabel = QLabel("开放源代码许可", self)
        self.aboutOpenSourceTextEdit = TextEdit(self)
        self.aboutOpenSourceVBox.addWidget(self.aboutOpenSourceLabel)
        self.aboutOpenSourceVBox.addWidget(self.aboutOpenSourceTextEdit)
        self.aboutVBox.addLayout(self.aboutOpenSourceVBox)

        self.aboutFeedbackVBox = QVBoxLayout(self)
        self.aboutFeedbackLabel = QLabel("反馈", self)
        self.aboutFeedbackDocumentHyperlink = HyperlinkCard(
            url='https://auroraziling.github.io/sangonomiya/',
            text="访问",
            parent=self,
            icon=FluentIcon.GLOBE,
            title="Sangonomiya 文档"
        )
        self.aboutFeedbackGithubIssueHyperlink = HyperlinkCard(
            url='https://github.com/AuroraZiling/sangonomiya/issues',
            text="提交",
            parent=self,
            icon=customIcon.MyFluentIcon.GITHUB,
            title="Github Issue"
        )
        self.aboutFeedbackGithubPullRequestHyperlink = HyperlinkCard(
            url='https://github.com/AuroraZiling/sangonomiya/pulls',
            text="提交",
            parent=self,
            icon=customIcon.MyFluentIcon.GITHUB,
            title="Github Pull Request"
        )
        self.aboutFeedbackVBox.addWidget(self.aboutFeedbackLabel)
        self.aboutFeedbackVBox.addWidget(self.aboutFeedbackDocumentHyperlink)
        self.aboutFeedbackVBox.addWidget(self.aboutFeedbackGithubIssueHyperlink)
        self.aboutFeedbackVBox.addWidget(self.aboutFeedbackGithubPullRequestHyperlink)
        self.aboutVBox.addLayout(self.aboutFeedbackVBox)

        self.aboutVBox.addStretch(1)

        self.setObjectName("AboutFrame")
        self.initGrid()
        self.initFrame()
        StyleSheet.ABOUT_FRAME.apply(self)
        log.infoWrite("[SubWidget][About] Initialized")

    def initGrid(self):
        # Top
        self.aboutTopHBox.insertSpacing(0, 15)
        self.aboutTopHBox.insertSpacing(2, 10)
        self.aboutVBox.insertSpacing(0, 10)

    def initFrame(self):
        # Top
        # Top - Project Description
        self.aboutTopProjImage.move(60, 50)
        self.aboutTopProjImage.setFixedSize(128, 128)
        self.aboutTopProjImage.setPixmap(QtGui.QPixmap(f"{utils.workingDir}/assets/avatar_rounded.png"))
        self.aboutTopProjImage.setScaledContents(True)
        self.aboutTopProjDesLabel.setFont(utils.getFont(30))
        self.aboutTopProjDesVersion.setFont(utils.getFont(12))
        self.aboutTopProjDesLicense.setFont(utils.getFont(12))
        self.aboutTopProjDesGithub.setStyleSheet("color: grey;")
        self.aboutTopProjDesGithub.setFont(utils.getFont(8))
        # Top - UI Design
        self.aboutTopUIImage.setFixedSize(85, 85)
        self.aboutTopUIImage.setPixmap(QtGui.QPixmap(f"{utils.workingDir}/assets/pyqt-fluent-widgets-logo.png"))
        self.aboutTopUIImage.setScaledContents(True)
        self.aboutTopUIDesDesignLabel.setStyleSheet("margin-bottom: 0px;")
        self.aboutTopUIDesDesignLabel.setFont(utils.getFont(8))
        self.aboutTopUIDesLabel.setStyleSheet("margin-top: 0px;")
        self.aboutTopUIDesLabel.setFont(utils.getFont(20))
        self.aboutTopUIDesVersion.setFont(utils.getFont(10))
        self.aboutTopUIDesGithub.setStyleSheet("color: grey;")
        self.aboutTopUIDesGithub.setFont(utils.getFont(7))
        # Open Source
        self.aboutOpenSourceLabel.setFont(utils.getFont(16))
        self.aboutOpenSourceTextEdit.setMinimumHeight(240)
        if isDarkTheme():
            self.aboutOpenSourceTextEdit.setStyleSheet("background-color: #323232; color: white;")
        self.aboutOpenSourceTextEdit.setFont(utils.getFont(10))
        self.aboutOpenSourceTextEdit.setReadOnly(True)
        self.aboutOpenSourceTextEdit.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.aboutOpenSourceTextEdit.setPlainText(utils.openSourceLicense)
        # Feedback
        self.aboutFeedbackLabel.setFont(utils.getFont(16))
        self.aboutFeedbackDocumentHyperlink.setFont(utils.getFont(12))
        self.aboutFeedbackGithubIssueHyperlink.setFont(utils.getFont(12))
        self.aboutFeedbackGithubPullRequestHyperlink.setFont(utils.getFont(12))
