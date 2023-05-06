# coding:utf-8
import os
import sys
import ctypes
import time

from PyQt6.QtCore import Qt, QTranslator
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QStackedWidget, QHBoxLayout

from qfluentwidgets import FluentIcon, NavigationInterface, NavigationItemPosition, setTheme, Theme, isDarkTheme
from qframelesswindow import FramelessWindow

from modules.Views import homeFrame, gachaReportFrame, linkFrame, announcementFrame, \
    settingFrame, aboutFrame
from modules.Scripts.UI import customIcon
from modules.Scripts.UI.titleBar import CustomTitleBar
from modules.Scripts.UI.styleSheet import StyleSheet
from modules.Scripts.Utils import ConfigUtils, logTracker as log

utils = ConfigUtils.ConfigUtils()

if not os.path.exists(utils.workingDir + "/logs/"):
    os.mkdir(utils.workingDir + "/logs/")

if sys.platform.startswith("win32"):
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

log.infoWrite("-----===== Sangonomiya Log =====-----")
log.infoWrite(f"Time: {time.strftime('%Y.%m.%d %H:%M:%S', time.localtime())}")
log.infoWrite(f"OS Platform: {sys.platform}")
log.infoWrite(f"Version: {utils.appVersion}")
log.infoWrite(f"Python Version: {sys.version}")
log.infoWrite(f"Working Directory: {utils.workingDir}")
log.infoWrite("-----===== Start Tracking =====-----")


class Window(FramelessWindow):

    def __init__(self):
        super().__init__()

        self.setTitleBar(CustomTitleBar(self))
        self.setWindowFlags(Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.MSWindowsFixedSizeDialogHint)

        self.mainHBoxLayout = QHBoxLayout(self)
        self.navigationInterface = NavigationInterface(self, showMenuButton=True)
        self.mainStackWidget = QStackedWidget(self)

        self.homeInterface = homeFrame.HomeWidget(self)
        self.gachaReportInterface = gachaReportFrame.GachaReportWidget(self)
        self.linkInterface = linkFrame.LinkWidget(self)
        self.announcementInterface = announcementFrame.AnnouncementWidget(self)
        self.settingInterface = settingFrame.SettingWidget(self)
        self.aboutInterface = aboutFrame.AboutWidget(self)

        self.mainStackWidget.addWidget(self.homeInterface)
        self.mainStackWidget.addWidget(self.gachaReportInterface)
        self.mainStackWidget.addWidget(self.linkInterface)
        self.mainStackWidget.addWidget(self.announcementInterface)
        self.mainStackWidget.addWidget(self.settingInterface)
        self.mainStackWidget.addWidget(self.aboutInterface)

        self.initLayout()
        self.initNavigation()
        self.initWindow()
        log.infoWrite("[UI] UI Initialized")

    def initLayout(self):
        self.mainHBoxLayout.setSpacing(0)
        self.mainHBoxLayout.setContentsMargins(0, self.titleBar.height(), 0, 0)
        self.mainHBoxLayout.addWidget(self.navigationInterface)
        self.mainHBoxLayout.addWidget(self.mainStackWidget)
        self.mainHBoxLayout.setStretchFactor(self.mainStackWidget, 1)

    def initNavigation(self):
        self.navigationInterface.addItem(
            routeKey=self.homeInterface.objectName(),
            icon=FluentIcon.HOME,
            text=self.tr("Home"),
            onClick=lambda: self.switchTo(self.homeInterface)
        )

        self.navigationInterface.addItem(
            routeKey=self.gachaReportInterface.objectName(),
            icon=customIcon.MyFluentIcon.GACHA_REPORT,
            text=self.tr("Gacha Report"),
            onClick=lambda: self.switchTo(self.gachaReportInterface)
        )
        self.navigationInterface.addItem(
            routeKey=self.linkInterface.objectName(),
            icon=customIcon.MyFluentIcon.DATA,
            text=self.tr("Import & Export Data"),
            onClick=lambda: self.switchTo(self.linkInterface)
        )
        self.navigationInterface.addItem(
            routeKey=self.announcementInterface.objectName(),
            icon=customIcon.MyFluentIcon.ANNOUNCEMENT,
            text=self.tr("Announcement"),
            onClick=lambda: self.switchTo(self.announcementInterface)
        )

        self.navigationInterface.addSeparator()

        self.navigationInterface.addItem(
            routeKey=self.settingInterface.objectName(),
            icon=FluentIcon.SETTING,
            text=self.tr("Settings"),
            onClick=lambda: self.switchTo(self.settingInterface),
            position=NavigationItemPosition.BOTTOM
        )

        self.navigationInterface.addItem(
            routeKey=self.aboutInterface.objectName(),
            icon=customIcon.MyFluentIcon.ABOUT,
            text=self.tr("About"),
            onClick=lambda: self.switchTo(self.aboutInterface),
            position=NavigationItemPosition.BOTTOM
        )
        self.navigationInterface.setExpandWidth(220)
        self.mainStackWidget.currentChanged.connect(self.onCurrentInterfaceChanged)
        self.onCurrentInterfaceChanged(0)

    def initWindow(self):
        self.setFixedSize(1200, 700)
        self.setWindowTitle('Sangonomiya')
        self.setWindowIcon(QIcon(f'{utils.workingDir}/assets/avatar.png'))
        self.titleBar.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        StyleSheet.MAIN_WINDOW.apply(self)

    def switchTo(self, widget):
        self.mainStackWidget.setCurrentWidget(widget)

    def onCurrentInterfaceChanged(self, index):
        widget = self.mainStackWidget.widget(index)
        self.navigationInterface.setCurrentItem(widget.objectName())
        log.infoWrite(f"[Sangonomiya] Current frame: {widget.objectName()}")


if __name__ == '__main__':
    log.infoWrite("[Sangonomiya] Main process starting")
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(f"{utils.workingDir}/assets/avatar.png"))
    try:
        if not utils.language == 'en_US':
            translator = QTranslator()
            if utils.language == "Auto":
                translator.load(f"{utils.workingDir}/languages/{utils.systemLanguage}.qm")
            else:
                translator.load(f"{utils.workingDir}/languages/{utils.language}.qm")
            app.installTranslator(translator)
    except FileNotFoundError:
        log.warningWrite(f"[Sangonomiya] Config file not found, using default language (en_US)")
        translator = QTranslator()
        translator.load(f"{utils.workingDir}/languages/{utils.systemLanguage}.qm")
        app.installTranslator(translator)
    log.infoWrite("[Sangonomiya] Language loaded")
    w = Window()
    w.show()
    app.exec()
