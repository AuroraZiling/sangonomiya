from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QLabel, QHBoxLayout
from ..Scripts.Utils import ConfigUtils

utils = ConfigUtils.ConfigUtils()

class HomeWidget(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.label = QLabel(self.tr("Working in progress..."), self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignmentFlag.AlignCenter)
        self.setObjectName("HomeFrame")
        self.initFrame()

    def initFrame(self):
        self.label.setFont(utils.getFont(40))
        self.label.setStyleSheet("color: white;")