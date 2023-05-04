from PyQt6.QtCore import Qt
from qfluentwidgets import InfoBar, InfoBarPosition

INFOBAR_POSITION_MAPPING = {
    "tl": InfoBarPosition.TOP_LEFT,
    "t": InfoBarPosition.TOP,
    "tr": InfoBarPosition.TOP_RIGHT,
    "bl": InfoBarPosition.BOTTOM_LEFT,
    "b": InfoBarPosition.BOTTOM,
    "br": InfoBarPosition.BOTTOM_RIGHT
}


def successBar(title, content, position, parent, isClosable=True, duration=2000):
    InfoBar.success(
        title=title,
        content=content,
        orient=Qt.Orientation.Horizontal,
        isClosable=isClosable,
        position=INFOBAR_POSITION_MAPPING[position],
        duration=duration,
        parent=parent
    )


def warningBar(title, content, position: InfoBarPosition, parent, isClosable=True, duration=2000):
    InfoBar.warning(
        title=title,
        content=content,
        orient=Qt.Orientation.Horizontal,
        isClosable=isClosable,
        position=INFOBAR_POSITION_MAPPING[position],
        duration=duration,
        parent=parent
    )


def errorBar(title, content, position: InfoBarPosition, parent, isClosable=True, duration=2000):
    InfoBar.error(
        title=title,
        content=content,
        orient=Qt.Orientation.Horizontal,
        isClosable=isClosable,
        position=INFOBAR_POSITION_MAPPING[position],
        duration=duration,
        parent=parent
    )
