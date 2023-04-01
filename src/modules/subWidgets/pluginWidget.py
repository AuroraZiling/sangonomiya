from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QLabel, QHBoxLayout


class PluginWidget(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.label = QLabel("PluginWidget", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignmentFlag.AlignCenter)
        self.setObjectName("PluginWidget")
        self.initFrame()

    def initFrame(self):
        self.label.setStyleSheet("color: white;")