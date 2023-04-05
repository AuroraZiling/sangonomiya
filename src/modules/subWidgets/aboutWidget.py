import sys

sys.path.append("..")

from PyQt6 import QtGui, QtWidgets
from PyQt6.QtWidgets import QFrame, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QSplitter

from qfluentwidgets import SettingCardGroup, HyperlinkCard, ExpandLayout, HyperlinkCard
from qfluentwidgets import FluentIcon

from components import OSUtils, customIcon

utils = OSUtils.OSUtils()


class AboutWidget(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.settingVBox = QVBoxLayout(self)

        self.settingTopHBox = QHBoxLayout(self)

        self.settingTopProjImage = QLabel("", self)
        self.settingTopHBox.addWidget(self.settingTopProjImage)

        self.settingTopProjDesVBox = QVBoxLayout(self)
        self.settingTopProjDesLabel = QLabel("Sangonomiya", self)
        self.settingTopProjDesVersion = QLabel(f"{utils.appVersion} for {utils.OSName}", self)
        self.settingTopProjDesLicense = QLabel("GPL v3.0", self)
        self.settingTopProjDesGithub = QLabel("https://github.com/AuroraZiling/sangonomiya", self)
        self.settingTopProjDesVBox.addWidget(self.settingTopProjDesLabel)
        self.settingTopProjDesVBox.addWidget(self.settingTopProjDesVersion)
        self.settingTopProjDesVBox.addWidget(self.settingTopProjDesLicense)
        self.settingTopProjDesVBox.addWidget(self.settingTopProjDesGithub)
        self.settingTopProjDesVBox.addStretch(1)
        self.settingTopHBox.addLayout(self.settingTopProjDesVBox)

        self.settingTopUIImage = QLabel("", self)
        self.settingTopHBox.addWidget(self.settingTopUIImage)

        self.settingTopUIDesVBox = QVBoxLayout(self)
        self.settingTopUIDesDesignLabel = QLabel("UI Design", self)
        self.settingTopUIDesLabel = QLabel("PyQt-Fluent-Widgets", self)
        self.settingTopUIDesVersion = QLabel(f"{utils.UIVersion} for PyQt6", self)
        self.settingTopUIDesGithub = QLabel("https://github.com/zhiyiYo/PyQt-Fluent-Widgets", self)
        self.settingTopUIDesVBox.addWidget(self.settingTopUIDesDesignLabel)
        self.settingTopUIDesVBox.addWidget(self.settingTopUIDesLabel)
        self.settingTopUIDesVBox.addWidget(self.settingTopUIDesVersion)
        self.settingTopUIDesVBox.addWidget(self.settingTopUIDesGithub)
        self.settingTopUIDesVBox.addStretch(1)

        self.settingTopHBox.addLayout(self.settingTopUIDesVBox)
        self.settingVBox.addLayout(self.settingTopHBox)

        self.settingOpenSourceVBox = QVBoxLayout(self)
        self.settingOpenSourceLabel = QLabel(self.tr("Open Source License"), self)
        self.settingOpenSourceTextEdit = QtWidgets.QTextEdit(self)
        self.settingOpenSourceVBox.addWidget(self.settingOpenSourceLabel)
        self.settingOpenSourceVBox.addWidget(self.settingOpenSourceTextEdit)
        self.settingVBox.addLayout(self.settingOpenSourceVBox)

        self.settingFeedbackVBox = QVBoxLayout(self)
        self.settingFeedbackLabel = QLabel(self.tr("Feedback"), self)
        self.settingFeedbackDocumentHyperlink = HyperlinkCard(
            url='https://auroraziling.github.io/sangonomiya/',
            text=self.tr('Open'),
            parent=self,
            icon=FluentIcon.WEB,
            title=self.tr('Sangonomiya Documents')
        )
        self.settingFeedbackGithubIssueHyperlink = HyperlinkCard(
            url='https://github.com/AuroraZiling/sangonomiya/issues',
            text=self.tr('Submit'),
            parent=self,
            icon=customIcon.MyFluentIcon.GITHUB,
            title=self.tr('Github Issue')
        )
        self.settingFeedbackGithubPullRequestHyperlink = HyperlinkCard(
            url='https://github.com/AuroraZiling/sangonomiya/pulls',
            text=self.tr('Submit'),
            parent=self,
            icon=customIcon.MyFluentIcon.GITHUB,
            title=self.tr('Github Pull Request')
        )
        self.settingFeedbackVBox.addWidget(self.settingFeedbackLabel)
        self.settingFeedbackVBox.addWidget(self.settingFeedbackDocumentHyperlink)
        self.settingFeedbackVBox.addWidget(self.settingFeedbackGithubIssueHyperlink)
        self.settingFeedbackVBox.addWidget(self.settingFeedbackGithubPullRequestHyperlink)
        self.settingVBox.addLayout(self.settingFeedbackVBox)

        self.settingVBox.addStretch(1)

        self.setObjectName("AboutWidget")
        self.initGrid()
        self.initFrame()

    def initGrid(self):
        # Top
        self.settingTopHBox.insertSpacing(0, 15)
        self.settingTopHBox.insertSpacing(2, 10)
        self.settingVBox.insertSpacing(0, 15)
        # Open Source
        self.settingVBox.insertSpacing(2, 20)
        self.settingOpenSourceVBox.insertSpacing(1, 10)
        # Feedback
        self.settingVBox.insertSpacing(4, 15)
        self.settingFeedbackVBox.insertSpacing(1, 10)

    def initFrame(self):
        # Top
        # Top - Project Description
        self.settingTopProjImage.move(50, 50)
        self.settingTopProjImage.setFixedSize(128, 128)
        self.settingTopProjImage.setPixmap(QtGui.QPixmap(f"{utils.workingDir}/assets/avatar_rounded.png"))
        self.settingTopProjImage.setScaledContents(True)
        self.settingTopProjDesLabel.setStyleSheet("color: white;")
        self.settingTopProjDesLabel.setFont(utils.getFont(30))
        self.settingTopProjDesVersion.setStyleSheet("color: white;")
        self.settingTopProjDesVersion.setFont(utils.getFont(12))
        self.settingTopProjDesLicense.setStyleSheet("color: white;")
        self.settingTopProjDesLicense.setFont(utils.getFont(12))
        self.settingTopProjDesGithub.setStyleSheet("color: grey;")
        self.settingTopProjDesGithub.setFont(utils.getFont(8))
        # Top - UI Design
        self.settingTopUIImage.setFixedSize(85, 85)
        self.settingTopUIImage.setPixmap(QtGui.QPixmap(f"{utils.workingDir}/assets/pyqt-fluent-widgets-logo.png"))
        self.settingTopUIImage.setScaledContents(True)
        self.settingTopUIDesDesignLabel.setStyleSheet("color: white; margin-bottom: 0px;")
        self.settingTopUIDesDesignLabel.setFont(utils.getFont(8))
        self.settingTopUIDesLabel.setStyleSheet("color: white; margin-top: 0px;")
        self.settingTopUIDesLabel.setFont(utils.getFont(20))
        self.settingTopUIDesVersion.setStyleSheet("color: white;")
        self.settingTopUIDesVersion.setFont(utils.getFont(10))
        self.settingTopUIDesGithub.setStyleSheet("color: grey;")
        self.settingTopUIDesGithub.setFont(utils.getFont(7))
        # Open Source
        self.settingOpenSourceLabel.setStyleSheet("color: white;")
        self.settingOpenSourceLabel.setFont(utils.getFont(16))
        self.settingOpenSourceTextEdit.setFixedHeight(220)
        self.settingOpenSourceTextEdit.setStyleSheet("background-color: #323232; color: white;")
        self.settingOpenSourceTextEdit.setFont(utils.getFont(10))
        self.settingOpenSourceTextEdit.setReadOnly(True)
        self.settingOpenSourceTextEdit.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.settingOpenSourceTextEdit.setPlainText(utils.openSourceLicense)
        # Feedback
        self.settingFeedbackLabel.setStyleSheet("color: white;")
        self.settingFeedbackLabel.setFont(utils.getFont(16))
        self.settingFeedbackDocumentHyperlink.setFont(utils.getFont(12))
        self.settingFeedbackGithubIssueHyperlink.setFont(utils.getFont(12))
        self.settingFeedbackGithubPullRequestHyperlink.setFont(utils.getFont(12))
