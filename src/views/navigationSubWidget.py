from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QFrame, QLabel, QHBoxLayout, QVBoxLayout

from qfluentwidgets import LineEdit, PrimaryPushButton, PushButton, ComboBox, ToolButton
from qfluentwidgets import FluentIcon as FIF


def fontSettings(size):
    return QFont("Microsoft YaHei", size)


class NavigationSubWidgetDemo(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignmentFlag.AlignCenter)
        self.setObjectName("demo")


class NavigationGachaReportWidget(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.label = QLabel("GachaReport", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignmentFlag.AlignCenter)
        self.setObjectName("gacha_report")


class NavigationSearchWidget(QFrame):

    def __init__(self, parent=None):
        super().__init__()

        self.searchVBox = QVBoxLayout(self)
        self.searchLabel = QLabel("Internationale", self)
        self.searchHBox = QHBoxLayout(self)
        self.searchComboBox = ComboBox(self)
        self.searchLineEdit = LineEdit('', self)
        self.searchBtn = ToolButton(FIF.SEARCH, self)
        self.searchVBox.addStretch(1)
        self.searchVBox.addWidget(self.searchLabel, 0, Qt.AlignmentFlag.AlignCenter)
        self.searchHBox.addStretch(1)
        self.searchHBox.addWidget(self.searchComboBox, 0, Qt.AlignmentFlag.AlignHCenter)
        self.searchHBox.addWidget(self.searchLineEdit, 0, Qt.AlignmentFlag.AlignHCenter)
        self.searchHBox.addWidget(self.searchBtn, 0, Qt.AlignmentFlag.AlignHCenter)
        self.searchHBox.addStretch(1)
        self.searchVBox.addLayout(self.searchHBox, 0)
        self.searchVBox.addStretch(1)
        self.setObjectName("search")
        self.initUI()

    def initUI(self):
        self.searchLabel.setFont(fontSettings(48))
        self.searchComboBox.setFixedSize(100, 33)
        self.searchComboBox.addItems(["书籍", "作者", "年份"])
        self.searchComboBox.setCurrentIndex(0)
        self.searchLineEdit.setFixedSize(400, 33)
        self.searchLineEdit.setClearButtonEnabled(True)
        self.searchBtn.setFixedSize(33, 33)
        self.searchBtn.setFont(fontSettings(14))


class NavigationFavoriteWidget(QFrame):

    def __init__(self, parent=None):
        super().__init__()
        self.label = QLabel("Favorite", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignmentFlag.AlignCenter)
        self.setObjectName("favorite")


class NavigationDownloadWidget(QFrame):

    def __init__(self, parent=None):
        super().__init__()
        self.label = QLabel("Download", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignmentFlag.AlignCenter)
        self.setObjectName("download")


class NavigationSettingsWidget(QFrame):

    def __init__(self, parent=None):
        super().__init__()
        self.label = QLabel("Settings", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignmentFlag.AlignCenter)
        self.setObjectName("settings")
