# coding:utf-8
import ctypes
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QStackedWidget, QHBoxLayout
from qfluentwidgets import FluentIcon
from qfluentwidgets import (NavigationInterface, NavigationItemPostion, setTheme, Theme, Dialog)
from qframelesswindow import FramelessWindow, StandardTitleBar

from components import themeManager, customIcon
from modules.subWidgets import gachaReportWidget, announcementWidget, accountWidget, pluginWidget, settingWidget

if sys.platform.startswith("win32"):
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")


class Window(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.setTitleBar(StandardTitleBar(self))

        setTheme(Theme.DARK)

        self.mainHBoxLayout = QHBoxLayout(self)
        self.navigationInterface = NavigationInterface(self, showMenuButton=True)
        self.mainStackWidget = QStackedWidget(self)

        self.gachaReportInterface = gachaReportWidget.GachaReportWidget(self)
        self.announcementInterface = announcementWidget.AnnouncementWidget(self)
        self.accountInterface = accountWidget.AccountWidget(self)
        self.pluginInterface = pluginWidget.PluginWidget(self)
        self.settingInterface = settingWidget.SettingWidget(self)

        self.mainStackWidget.addWidget(self.gachaReportInterface)
        self.mainStackWidget.addWidget(self.announcementInterface)
        self.mainStackWidget.addWidget(self.accountInterface)
        self.mainStackWidget.addWidget(self.pluginInterface)
        self.mainStackWidget.addWidget(self.settingInterface)

        self.initLayout()
        self.initNavigation()
        self.initWindow()

    def initLayout(self):
        self.mainHBoxLayout.setSpacing(0)
        self.mainHBoxLayout.setContentsMargins(0, self.titleBar.height(), 0, 0)
        self.mainHBoxLayout.addWidget(self.navigationInterface)
        self.mainHBoxLayout.addWidget(self.mainStackWidget)
        self.mainHBoxLayout.setStretchFactor(self.mainStackWidget, 1)

    def initNavigation(self):
        self.navigationInterface.addItem(
            routeKey=self.gachaReportInterface.objectName(),
            icon=customIcon.MyFluentIcon.GACHA_REPORT,
            text='祈愿记录 / Gacha Report',
            onClick=lambda: self.switchTo(self.gachaReportInterface)
        )
        self.navigationInterface.addItem(
            routeKey=self.announcementInterface.objectName(),
            icon=customIcon.MyFluentIcon.ANNOUNCEMENT,
            text='公告 / Announcement',
            onClick=lambda: self.switchTo(self.announcementInterface)
        )

        self.navigationInterface.addSeparator()

        self.navigationInterface.addItem(
            routeKey=self.accountInterface.objectName(),
            icon=customIcon.MyFluentIcon.USER,
            text='账户 / Account',
            onClick=lambda: self.switchTo(self.accountInterface),
            position=NavigationItemPostion.BOTTOM
        )

        self.navigationInterface.addItem(
            routeKey=self.pluginInterface.objectName(),
            icon=customIcon.MyFluentIcon.PLUGIN,
            text='插件 / Plugins',
            onClick=lambda: self.switchTo(self.pluginInterface),
            position=NavigationItemPostion.BOTTOM
        )

        self.navigationInterface.addItem(
            routeKey=self.settingInterface.objectName(),
            icon=FluentIcon.SETTING,
            text='设置 / Settings',
            onClick=lambda: self.switchTo(self.settingInterface),
            position=NavigationItemPostion.BOTTOM
        )

        self.navigationInterface.setExpandWidth(230)

        self.mainStackWidget.currentChanged.connect(self.onCurrentInterfaceChanged)
        self.mainStackWidget.setCurrentIndex(1)

    def initWindow(self):
        self.resize(900, 700)
        self.setWindowTitle('Sangonomiya')
        self.setWindowIcon(QIcon(f"assets/avatar.png"))
        self.titleBar.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        self.setStyleSheet(themeManager.setTheme("dark"))

    def switchTo(self, widget):
        self.mainStackWidget.setCurrentWidget(widget)

    def onCurrentInterfaceChanged(self, index):
        widget = self.mainStackWidget.widget(index)
        self.navigationInterface.setCurrentItem(widget.objectName())

    def showMessageBox(self, title, content):
        dialog = Dialog(title, content, self)
        if dialog.exec():
            print('Yes button is pressed')
        else:
            print('Cancel button is pressed')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec()
