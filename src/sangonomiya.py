# coding:utf-8
import sys
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QIcon, QPainter, QImage, QBrush, QColor, QFont
from PySide6.QtWidgets import QApplication, QFrame, QStackedWidget, QHBoxLayout, QLabel

from qfluentwidgets import (NavigationInterface, NavigationItemPostion, NavigationWidget, MessageBox,
                            isDarkTheme, setTheme, Theme, setThemeColor)
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import FramelessWindow, StandardTitleBar

from components.avatarWidget import AvatarWidget
from components import messageBox as msgBox


class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = QLabel(text, self)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))


class Window(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.setTitleBar(StandardTitleBar(self))

        # use dark theme mode
        setTheme(Theme.DARK)
        self.messageBox = msgBox.MessageBoxUtil(self)

        # change the theme color
        # setThemeColor('#0078d4')

        self.hBoxLayout = QHBoxLayout(self)
        self.navigationInterface = NavigationInterface(self, showMenuButton=True)
        self.stackWidget = QStackedWidget(self)

        # create sub interface
        self.searchInterface = Widget('Search Interface', self)
        self.musicInterface = Widget('Music Interface', self)
        self.videoInterface = Widget('Video Interface', self)
        self.folderInterface = Widget('Folder Interface', self)
        self.settingInterface = Widget('Setting Interface', self)

        self.stackWidget.addWidget(self.searchInterface)
        self.stackWidget.addWidget(self.musicInterface)
        self.stackWidget.addWidget(self.videoInterface)
        self.stackWidget.addWidget(self.folderInterface)
        self.stackWidget.addWidget(self.settingInterface)

        # initialize layout
        self.initLayout()

        # add items to navigation interface
        self.initNavigation()

        self.initWindow()

    def initLayout(self):
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, self.titleBar.height(), 0, 0)
        self.hBoxLayout.addWidget(self.navigationInterface)
        self.hBoxLayout.addWidget(self.stackWidget)
        self.hBoxLayout.setStretchFactor(self.stackWidget, 1)

    def initNavigation(self):
        self.navigationInterface.addItem(
            routeKey=self.searchInterface.objectName(),
            icon=FIF.SEARCH,
            text='Search',
            onClick=lambda: self.switchTo(self.searchInterface)
        )
        self.navigationInterface.addItem(
            routeKey=self.musicInterface.objectName(),
            icon=FIF.MUSIC,
            text='Music library',
            onClick=lambda: self.switchTo(self.musicInterface)
        )
        self.navigationInterface.addItem(
            routeKey=self.videoInterface.objectName(),
            icon=FIF.VIDEO,
            text='Video library',
            onClick=lambda: self.switchTo(self.videoInterface)
        )

        self.navigationInterface.addSeparator()

        # add navigation items to scroll area
        self.navigationInterface.addItem(
            routeKey=self.folderInterface.objectName(),
            icon=FIF.FOLDER,
            text='Folder library',
            onClick=lambda: self.switchTo(self.folderInterface),
            position=NavigationItemPostion.SCROLL
        )

        self.navigationInterface.addWidget(
            routeKey='avatar',
            widget=AvatarWidget(),
            onClick=self.messageBox.show(""),
            position=NavigationItemPostion.BOTTOM
        )

        self.navigationInterface.addItem(
            routeKey=self.settingInterface.objectName(),
            icon=FIF.SETTING,
            text='Settings',
            onClick=lambda: self.switchTo(self.settingInterface),
            position=NavigationItemPostion.BOTTOM
        )

        self.navigationInterface.setExpandWidth(200)

        self.stackWidget.currentChanged.connect(self.onCurrentInterfaceChanged)
        self.stackWidget.setCurrentIndex(1)

    def initWindow(self):
        self.resize(900, 700)
        self.setWindowTitle("Sangonomiya 珊瑚宫")
        self.titleBar.setAttribute(Qt.WA_StyledBackground)

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        self.setQss()

    def setQss(self):
        color = 'dark' if isDarkTheme() else 'light'
        with open(f'assets/themes/{color}.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def switchTo(self, widget):
        self.stackWidget.setCurrentWidget(widget)

    def onCurrentInterfaceChanged(self, index):
        widget = self.stackWidget.widget(index)
        self.navigationInterface.setCurrentItem(widget.objectName())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec()
