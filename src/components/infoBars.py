from PyQt6.QtCore import Qt
from qfluentwidgets import InfoBar, InfoBarPosition


def successBar(title, content, position: InfoBarPosition, parent, isClosable=True, duration=2000):
    InfoBar.success(
        title=title,
        content=content,
        orient=Qt.Orientation.Horizontal,
        isClosable=isClosable,
        position=position,
        duration=duration,
        parent=parent
    )


def warningBar(title, content, position: InfoBarPosition, parent, isClosable=True, duration=2000):
    InfoBar.warning(
        title=title,
        content=content,
        orient=Qt.Orientation.Horizontal,
        isClosable=isClosable,
        position=position,
        duration=duration,
        parent=parent
    )


def errorBar(title, content, position: InfoBarPosition, parent, isClosable=True, duration=2000):
    InfoBar.error(
        title=title,
        content=content,
        orient=Qt.Orientation.Horizontal,
        isClosable=isClosable,
        position=position,
        duration=duration,
        parent=parent
    )
