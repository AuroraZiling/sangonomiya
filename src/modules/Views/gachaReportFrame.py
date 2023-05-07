from PySide6 import QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QHBoxLayout, QVBoxLayout, QAbstractItemView, QTextEdit, QHeaderView, \
    QWidget, QTableWidgetItem
from .ViewConfigs.config import cfg
from ..Scripts.Utils import ConfigUtils
from ..Core.GachaReport.gachaReportThread import GachaReportThread
from ..Scripts.UI.styleSheet import StyleSheet
from ..Scripts.UI.customDialog import URLDialog
from ..Core.GachaReport.gachaReportUtils import getDefaultGameDataPath, convertAPI
from ..Core.GachaReport import gachaReportRead
from ..Core.GachaReport.Analysis import tableCompletion
from ..Core.GachaReport.MihoyoAPI import byWebCache
from qfluentwidgets import FluentIcon, RoundMenu, TableWidget, TextEdit, MessageBox, Dialog, InfoBarPosition, ComboBox, \
    Action, InfoBar, PushButton, StateToolTip

from qfluentwidgets import DropDownPushButton

utils = ConfigUtils.ConfigUtils()

GACHATYPE_TO_CODE = {"角色活动祈愿": "301", "武器祈愿": "302", "常驻祈愿": "200"}


class GachaReportWidget(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.frameMessageBox = None
        self.isInteractive = False

        self.completedOriginalTableData = {}
        self.currentUID = ""

        # Gacha Report Thread
        self.gachaReportThreadStateTooltip = None
        self.gachaReportThread = None

        self.baseVBox = QVBoxLayout(self)

        self.headerHBox = QHBoxLayout()
        self.headerLeftVBox = QVBoxLayout()
        self.headerLeftGachaReportTitleLabel = QLabel("祈愿记录")
        self.headerLeftGachaReportUIDLabel = QLabel("未知的UID")
        self.headerLeftVBox.addWidget(self.headerLeftGachaReportTitleLabel)
        self.headerLeftVBox.addWidget(self.headerLeftGachaReportUIDLabel)

        self.headerRightHBox = QHBoxLayout()
        self.headerRightGachaTypeCombobox = ComboBox(self)
        self.headerRightUIDSelectCombobox = ComboBox(self)
        self.headerRightFullUpdateDropBtn = DropDownPushButton("全量更新", self, FluentIcon.UPDATE)
        self.headerRightFullUpdateDropBtnWebCacheAction = Action(FluentIcon.DOCUMENT.icon(), "网页缓存获取")
        self.headerRightFullUpdateDropBtnURLAction = Action(FluentIcon.ALIGNMENT.icon(), "手动URL获取")
        self.headerRightHBox.addWidget(self.headerRightGachaTypeCombobox)
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
        self.bottomRightBasicLabel = QLabel("基本数据")
        self.bottomRightBasicTotalLabel = QLabel("未知抽数")
        self.bottomRightBasicLevel5TotalLabel = QLabel("未知5星数量")
        self.bottomRightBasicLevel5TotalTextEdit = TextEdit()
        self.bottomRightBasicLevel4TotalLabel = QLabel("未知4星数量")
        self.bottomRightBasicLevel4TotalTextEdit = TextEdit()
        self.bottomRightBasicLevel3TotalLabel = QLabel("未知3星数量")
        self.bottomRightAnalysisLabel = QLabel("保底情况")
        self.bottomRightWeaponAlertLabel = QLabel("对于武器的保底分析会不准确")
        self.bottomRightAnalysisGuaranteeLabel = QLabel("未知")
        self.bottomRightGraphBtn = PushButton("图像", self)
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

        self.initData()

    def __gachaReportThreadStateTooltipClosed(self):
        self.gachaReportThread.exit(0)
        self.gachaReportStatusChanged((1, "Operation cancelled"))
        InfoBar.warning("操作终止", "数据读取已停止",
                        position=InfoBarPosition.BOTTOM, parent=self)

    def gachaReportStatusChanged(self, msg: tuple):
        if msg and self.gachaReportThreadStateTooltip:
            self.setInteractive(False)
            self.headerRightGachaTypeCombobox.setEnabled(False)
            self.gachaReportThreadStateTooltip.setContent(msg[1])
            if len(msg) == 3:
                self.gachaReportThreadStateTooltip.setTitle(f"更新数据中 | {msg[2]}")
            if msg[0] == 1:
                self.setInteractive(True)
                self.gachaReportThreadStateTooltip.setState(True)
                self.gachaReportThreadStateTooltip = None
                self.headerRightFullUpdateDropBtn.setEnabled(True)
                self.headerRightGachaTypeCombobox.setEnabled(True)
                self.initData()
                self.headerRightUIDSelectCombobox.setCurrentText(msg[2])
        else:
            self.headerRightFullUpdateDropBtn.setEnabled(True)

    def __headerRightFullUpdateDropBtnWebCache(self):
        gachaURL = convertAPI(byWebCache.getURL(getDefaultGameDataPath()))
        if gachaURL:
            resp = MessageBox("成功", "请求已被获取，是否更新数据?", self)
            if resp.exec():
                self.headerRightFullUpdateDropBtn.setEnabled(False)
                self.gachaReportThread = GachaReportThread(gachaURL)
                self.gachaReportThreadStateTooltip = StateToolTip("更新数据中", "数据更新开始",
                                                                  self)
                self.gachaReportThreadStateTooltip.closedSignal.connect(self.__gachaReportThreadStateTooltipClosed)
                self.gachaReportThreadStateTooltip.move(5, 5)
                self.gachaReportThreadStateTooltip.show()
                self.gachaReportThread.start()
                self.gachaReportThread.trigger.connect(self.gachaReportStatusChanged)
        else:
            MessageBox("失败", "无法从游戏缓存中获取请求", self)

    def __headerRightFullUpdateDropBtnURL(self):
        w = URLDialog("输入URL", "请在下方输入MiHoyoAPI的URL", self)
        w.returnSignal.connect(self.__headerRightFullUpdateDropBtnURLReturnSignal)
        w.exec()

    def __headerRightFullUpdateDropBtnURLReturnSignal(self, gachaURL: str):
        gachaURL = gachaURL.split("game_biz=hk4e_cn")[0] + "game_biz=hk4e_cn"
        if gachaURL:
            self.headerRightFullUpdateDropBtn.setEnabled(False)
            self.gachaReportThread = GachaReportThread(gachaURL)
            self.gachaReportThreadStateTooltip = StateToolTip("更新数据中", "数据更新开始", self)
            self.gachaReportThreadStateTooltip.closedSignal.connect(self.__gachaReportThreadStateTooltipClosed)
            self.gachaReportThreadStateTooltip.move(5, 5)
            self.gachaReportThreadStateTooltip.show()
            self.gachaReportThread.start()
            self.gachaReportThread.trigger.connect(self.gachaReportStatusChanged)

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
        if not gachaReportRead.getUIDList():
            self.setInteractive(False)
            InfoBar.warning("警告", "找不到UID",
                            position=InfoBarPosition.BOTTOM_RIGHT, parent=self)
        else:
            self.initData()
            self.setInteractive(True)

    def initFrame(self):
        self.headerLeftGachaReportTitleLabel.setFont(utils.getFont(18))
        self.headerLeftGachaReportUIDLabel.setStyleSheet("color: grey;")
        self.headerRightGachaTypeCombobox.setFixedWidth(200)
        self.headerRightGachaTypeCombobox.addItems(["角色活动祈愿", "武器祈愿", "常驻祈愿"])
        self.headerRightGachaTypeCombobox.setEnabled(False)
        self.headerRightGachaTypeCombobox.currentIndexChanged.connect(self.__headerRightGachaTypeComboboxChanged)
        self.headerRightUIDSelectCombobox.setFixedWidth(200)
        self.headerRightUIDSelectCombobox.currentIndexChanged.connect(self.__headerRightUIDSelectComboboxChanged)
        self.headerRightFullUpdateDropBtn.setFixedWidth(200)
        self.headerRightFullUpdateDropBtn.setMenu(self.headerRightFullUpdateDropBtnMenu)

        self.bottomLeftGachaTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.bottomLeftGachaTable.resizeColumnsToContents()
        self.bottomLeftGachaTable.setColumnCount(5)
        self.bottomLeftGachaTable.verticalHeader().setHidden(True)
        self.bottomLeftGachaTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.bottomLeftGachaTable.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.bottomLeftGachaTable.setHorizontalHeaderLabels(
            ["序号", "类型", "名称", "获取时间", "十连/单抽"])

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

    def tableUpdateData(self, currentData):
        for index, each in enumerate(currentData):
            for eachColumn in range(0, 5):
                self.bottomLeftGachaTable.setItem(index, eachColumn, QTableWidgetItem())
                self.bottomLeftGachaTable.setRowHeight(index, 40)
                self.bottomLeftGachaTable.item(index, eachColumn).setText(each[eachColumn])

    def __headerRightGachaTypeComboboxChanged(self):
        if not self.completedOriginalTableData:
            self.currentUID = self.headerRightUIDSelectCombobox.currentText()
            tableOriginalData = gachaReportRead.convertDataToTable(gachaReportRead.getDataFromUID(self.currentUID))
            self.completedOriginalTableData = tableCompletion.originalTableDataToComplete(tableOriginalData)
        currentTableData = self.completedOriginalTableData[
            GACHATYPE_TO_CODE[self.headerRightGachaTypeCombobox.currentText()]]
        self.bottomLeftGachaTable.setRowCount(len(currentTableData))
        self.tableUpdateData(currentTableData)

    def __headerRightUIDSelectComboboxChanged(self):
        currentUID = self.headerRightUIDSelectCombobox.currentText()
        if currentUID:
            self.headerLeftGachaReportUIDLabel.setText(currentUID)
            self.headerRightGachaTypeCombobox.setEnabled(True)
            tableOriginalData = gachaReportRead.convertDataToTable(gachaReportRead.getDataFromUID(currentUID))
            self.completedOriginalTableData = tableCompletion.originalTableDataToComplete(tableOriginalData)

            if not self.headerRightGachaTypeCombobox.currentText():
                self.headerRightGachaTypeCombobox.setCurrentIndex(0)
            self.__headerRightGachaTypeComboboxChanged()

            cfg.set(cfg.gachaReportLastUID, currentUID)
        else:
            cfg.set(cfg.gachaReportLastUID, "")

    def initData(self):
        self.headerRightUIDSelectCombobox.clear()
        self.headerRightUIDSelectCombobox.addItems(gachaReportRead.getUIDList())
        self.currentUID = cfg.gachaReportLastUID.value
        if self.currentUID:
            self.headerRightUIDSelectCombobox.setCurrentText(self.currentUID)
            self.__headerRightUIDSelectComboboxChanged()