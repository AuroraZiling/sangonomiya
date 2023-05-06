from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QLabel, QHBoxLayout, QVBoxLayout, QAbstractItemView, QTextEdit, QHeaderView, QWidget
from ..Scripts.Utils import ConfigUtils
from ..Core.GachaReport.gachaReportThread import GachaReportThread
from ..Scripts.UI.styleSheet import StyleSheet
from ..Core.GachaReport.gachaReportUtils import getDefaultGameDataPath, convertAPI
from ..Core.GachaReport.MihoyoAPI import byWebCache
from qfluentwidgets import FluentIcon, RoundMenu, TableWidget, TextEdit, MessageBox, Dialog, InfoBarPosition, ComboBox, \
    Action, InfoBar, PushButton, StateToolTip

from qfluentwidgets import DropDownPushButton

utils = ConfigUtils.ConfigUtils()


class GachaReportWidget(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.frameMessageBox = None
        self.isInteractive = False

        # Gacha Report Thread
        self.gachaReportThreadStateTooltip = None
        self.gachaReportThread = None

        self.baseVBox = QVBoxLayout(self)

        self.headerHBox = QHBoxLayout()
        self.headerLeftVBox = QVBoxLayout()
        self.headerLeftGachaReportTitleLabel = QLabel(self.tr("Gacha Report"))
        self.headerLeftGachaReportUIDLabel = QLabel(f"{self.tr('Unknown UID')}")
        self.headerLeftVBox.addWidget(self.headerLeftGachaReportTitleLabel)
        self.headerLeftVBox.addWidget(self.headerLeftGachaReportUIDLabel)

        self.headerRightHBox = QHBoxLayout()
        self.headerRightUIDSelectCombobox = ComboBox(self)
        self.headerRightFullUpdateDropBtn = DropDownPushButton(self.tr("Full update"), self, FluentIcon.UPDATE)
        self.headerRightFullUpdateDropBtnWebCacheAction = Action(FluentIcon.DOCUMENT.icon(), self.tr("Web Cache Mode"))
        self.headerRightFullUpdateDropBtnURLAction = Action(FluentIcon.ALIGNMENT.icon(), self.tr("URL Mode"))
        self.headerRightHBox.addWidget(self.headerRightUIDSelectCombobox)
        self.headerRightHBox.addWidget(self.headerRightFullUpdateDropBtn)
        self.headerRightFullUpdateDropBtnMenu = RoundMenu(parent=self)
        self.headerHBox.addLayout(self.headerLeftVBox)
        self.headerHBox.addLayout(self.headerRightHBox)

        self.bottomHBox = QHBoxLayout()
        self.bottomLeftVBox = QVBoxLayout()
        self.bottomLeftGachaTable = TableWidget()
        self.bottomLeftVBox.addWidget(self.bottomLeftGachaTable)

        self.bottomRightVBox = QVBoxLayout()
        self.bottomRightBasicLabel = QLabel(self.tr("Basic"))
        self.bottomRightBasicTotalLabel = QLabel(self.tr("Unknown amount"))
        self.bottomRightBasicLevel5TotalLabel = QLabel(self.tr("Unknown Level-5 amount"))
        self.bottomRightBasicLevel5TotalTextEdit = TextEdit()
        self.bottomRightBasicLevel4TotalLabel = QLabel(self.tr("Unknown Level-4 amount"))
        self.bottomRightBasicLevel4TotalTextEdit = TextEdit()
        self.bottomRightBasicLevel3TotalLabel = QLabel(self.tr("Unknown Level-3 amount"))
        self.bottomRightAnalysisLabel = QLabel(self.tr("Guarantee"))
        self.bottomRightWeaponAlertLabel = QLabel(self.tr("Analysis of weapons may be incomplete"))
        self.bottomRightAnalysisGuaranteeLabel = QLabel(self.tr("Unknown"))
        self.bottomRightGraphBtn = PushButton(self.tr("Graph"), self)
        self.bottomRightVBox.addWidget(self.bottomRightBasicLabel)
        self.bottomRightVBox.addWidget(self.bottomRightBasicTotalLabel)
        self.bottomRightVBox.addWidget(self.bottomRightBasicLevel5TotalLabel)
        self.bottomRightVBox.addWidget(self.bottomRightBasicLevel5TotalTextEdit)
        self.bottomRightVBox.addWidget(self.bottomRightBasicLevel4TotalLabel)
        self.bottomRightVBox.addWidget(self.bottomRightBasicLevel4TotalTextEdit)
        self.bottomRightVBox.addWidget(self.bottomRightBasicLevel3TotalLabel)
        self.bottomRightVBox.addWidget(self.bottomRightAnalysisLabel)
        self.bottomRightVBox.addWidget(self.bottomRightWeaponAlertLabel)
        self.bottomRightVBox.addWidget(self.bottomRightAnalysisGuaranteeLabel)
        self.bottomRightVBox.addWidget(self.bottomRightGraphBtn)

        self.bottomHBox.addLayout(self.bottomLeftVBox)
        self.bottomHBox.addLayout(self.bottomRightVBox)

        self.baseVBox.addLayout(self.headerHBox)
        self.baseVBox.addLayout(self.bottomHBox)

        self.setObjectName("GachaReportFrame")
        StyleSheet.GACHA_REPORT_FRAME.apply(self)
        self.initHeaderRightFullUpdateDropBtnActions()
        self.initFrame()

    def __gachaReportThreadStateTooltipClosed(self):
        self.gachaReportThread.exit(0)
        self.gachaReportStatusChanged((1, "Operation cancelled"))
        InfoBar.warning(self.tr("Operation interrupted"), self.tr("You have terminated data reading"),
                        position=InfoBarPosition.BOTTOM, parent=self)

    def gachaReportStatusChanged(self, msg: tuple):
        if msg and self.gachaReportThreadStateTooltip:
            self.gachaReportThreadStateTooltip.setContent(msg[1])
            if msg[0] == 1:
                self.gachaReportThreadStateTooltip.setState(True)
                self.gachaReportThreadStateTooltip = None
                self.headerRightFullUpdateDropBtn.setEnabled(True)
        else:
            self.headerRightFullUpdateDropBtn.setEnabled(True)

    def __headerRightFullUpdateDropBtnWebCache(self):
        gachaURL = convertAPI(byWebCache.getURL(getDefaultGameDataPath()))
        if gachaURL:
            resp = MessageBox(self.tr("Detected"), self.tr("Request has been acquired.\nUpdate data or not?"), self)
            if resp.exec():
                self.headerRightFullUpdateDropBtn.setEnabled(False)
                self.gachaReportThread = GachaReportThread(gachaURL)
                self.gachaReportThreadStateTooltip = StateToolTip(self.tr("Fetching"), self.tr("Start fetching data"),
                                                                  self)
                self.gachaReportThreadStateTooltip.closedSignal.connect(self.__gachaReportThreadStateTooltipClosed)
                self.gachaReportThreadStateTooltip.move(5, 5)
                self.gachaReportThreadStateTooltip.show()
                self.gachaReportThread.start()
                self.gachaReportThread.trigger.connect(self.gachaReportStatusChanged)
        else:
            MessageBox(self.tr("Undetected"), self.tr("Unable to fetch requests from the game web cache."), self)

    def __headerRightFullUpdateDropBtnURL(self):
        print(3)

    def initHeaderRightFullUpdateDropBtnActions(self):
        self.headerRightFullUpdateDropBtnWebCacheAction.triggered.connect(self.__headerRightFullUpdateDropBtnWebCache)
        self.headerRightFullUpdateDropBtnURLAction.triggered.connect(self.__headerRightFullUpdateDropBtnURL)
        self.headerRightFullUpdateDropBtnMenu.addAction(self.headerRightFullUpdateDropBtnWebCacheAction)
        self.headerRightFullUpdateDropBtnMenu.addAction(self.headerRightFullUpdateDropBtnURLAction)

    def setInteractive(self, mode):
        self.bottomLeftGachaTable.setEnabled(mode)
        self.headerRightUIDSelectCombobox.setEnabled(mode)
        self.bottomRightBasicLevel5TotalTextEdit.setEnabled(mode)
        self.bottomRightBasicLevel4TotalTextEdit.setEnabled(mode)
        self.bottomRightGraphBtn.setEnabled(mode)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        if utils.getAccountUid() == 0:
            self.setInteractive(False)
            InfoBar.warning(self.tr("Warning"), self.tr("No account information found"),
                            position=InfoBarPosition.BOTTOM_RIGHT, parent=self)
        else:
            self.setInteractive(True)

    def initFrame(self):
        self.headerLeftGachaReportTitleLabel.setFont(utils.getFont(18))
        self.headerLeftGachaReportUIDLabel.setStyleSheet("color: grey;")
        self.headerRightUIDSelectCombobox.setFixedWidth(200)
        self.headerRightFullUpdateDropBtn.setFixedWidth(200)
        self.headerRightFullUpdateDropBtn.setMenu(self.headerRightFullUpdateDropBtnMenu)

        self.bottomLeftGachaTable.setRowCount(60)
        self.bottomLeftGachaTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.bottomLeftGachaTable.resizeColumnsToContents()
        self.bottomLeftGachaTable.setColumnCount(5)
        self.bottomLeftGachaTable.verticalHeader().setHidden(True)
        self.bottomLeftGachaTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.bottomLeftGachaTable.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.bottomLeftGachaTable.setHorizontalHeaderLabels(
            [self.tr("ID"), self.tr("Type"), self.tr("Name"), self.tr("Time"), self.tr("Mode")])

        self.bottomRightBasicLabel.setFont(utils.getFont(14))
        self.bottomRightBasicTotalLabel.setFont(utils.getFont(12))
        self.bottomRightBasicLevel5TotalLabel.setFont(utils.getFont(10))
        self.bottomRightBasicLevel4TotalLabel.setFont(utils.getFont(10))
        self.bottomRightBasicLevel3TotalLabel.setFont(utils.getFont(10))
        self.bottomRightBasicLevel5TotalTextEdit.setReadOnly(True)
        self.bottomRightBasicLevel4TotalTextEdit.setReadOnly(True)

        self.bottomRightAnalysisLabel.setFont(utils.getFont(14))
        self.bottomRightWeaponAlertLabel.setFont(utils.getFont(10))
        self.bottomRightWeaponAlertLabel.setVisible(False)
        self.bottomRightAnalysisGuaranteeLabel.setFont(utils.getFont(10))
