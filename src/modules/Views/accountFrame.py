from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QHBoxLayout
from ..Scripts.Utils import ConfigUtils

utils = ConfigUtils.ConfigUtils()


class AccountWidget(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.label = QLabel("暂未开放", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignmentFlag.AlignCenter)
        self.setObjectName("AccountFrame")
        self.initFrame()

    def initFrame(self):
        self.label.setFont(utils.getFont(40))