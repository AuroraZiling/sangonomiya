from PyQt6.QtCore import Qt
from qfluentwidgets import InfoBar, InfoBarPosition


def successBar(title, content, parent):
    InfoBar.success(
        title=title,
        content=content,
        orient=Qt.Orientation.Horizontal,
        isClosable=True,
        position=InfoBarPosition.BOTTOM_RIGHT,
        duration=2000,
        parent=parent
    )


def warningBar(title, content, parent):
    InfoBar.warning(
        title=title,
        content=content,
        orient=Qt.Orientation.Horizontal,
        isClosable=True,
        position=InfoBarPosition.BOTTOM_RIGHT,
        duration=2000,
        parent=parent
    )


def errorBar(title, content, parent):
    InfoBar.error(
        title=title,
        content=content,
        orient=Qt.Orientation.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=2000,
        parent=parent
    )
