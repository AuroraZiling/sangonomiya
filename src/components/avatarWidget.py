from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QImage, QPainter, QColor, QBrush
from qfluentwidgets import NavigationWidget, isDarkTheme
import sys

sys.path.append("..")

from components import OSUtils

WORKING_DIR = OSUtils.getWorkingDir()


class AvatarWidget(NavigationWidget):
    """ Avatar widget """

    def __init__(self, account_name="未知", parent=None):
        super().__init__(isSelectable=False, parent=parent)
        self.account_name = account_name
        self.avatar = QImage(f"{WORKING_DIR}/assets/avatar.jpg").scaled(
            24, 24, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.RenderHint.SmoothPixmapTransform | QPainter.RenderHint.Antialiasing)

        painter.setPen(Qt.PenStyle.NoPen)

        if self.isPressed:
            painter.setOpacity(0.7)

        if self.isEnter:
            c = 255 if isDarkTheme() else 0
            painter.setBrush(QColor(c, c, c, 10))
            painter.drawRoundedRect(self.rect(), 5, 5)

        painter.setBrush(QBrush(self.avatar))
        painter.translate(8, 6)
        painter.drawEllipse(0, 0, 24, 24)
        painter.translate(-8, -6)

        if not self.isCompacted:
            painter.setPen(Qt.GlobalColor.white if isDarkTheme() else Qt.GlobalColor.black)
            painter.setFont(OSUtils.getFont(11))
            painter.drawText(QRect(44, 0, 255, 36), Qt.AlignmentFlag.AlignVCenter, self.account_name)
