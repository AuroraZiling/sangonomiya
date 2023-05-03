from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QFrame, QLabel, QHBoxLayout, QVBoxLayout, QAbstractItemView, QTextEdit, QHeaderView, QWidget
from components import OSUtils, downloader, infoBars
from pyqt6_plugins.examplebuttonplugin import QtGui
from qfluentwidgets import FluentIcon, RoundMenu, TableWidget, TextEdit, MessageBox, Dialog, InfoBarPosition

from qfluentwidgets import DropDownPushButton

utils = OSUtils.OSUtils()


class GachaReportWidget(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.frameMessageBox = None

        self.baseVBox = QVBoxLayout(self)

        self.headerHBox = QHBoxLayout()
        self.headerLeftVBox = QVBoxLayout()
        self.headerLeftGachaReportTitleLabel = QLabel(self.tr("Gacha Report"))
        self.headerLeftGachaReportUIDLabel = QLabel(f"{self.tr('Unknown UID')}")
        self.headerLeftVBox.addWidget(self.headerLeftGachaReportTitleLabel)
        self.headerLeftVBox.addWidget(self.headerLeftGachaReportUIDLabel)

        self.headerRightHBox = QHBoxLayout()
        self.headerRightFullUpdateDropBtn = DropDownPushButton(self.tr("Full update"), self, FluentIcon.UPDATE)
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

        self.bottomHBox.addLayout(self.bottomLeftVBox)
        self.bottomHBox.addLayout(self.bottomRightVBox)

        self.baseVBox.addLayout(self.headerHBox)
        self.baseVBox.addLayout(self.bottomHBox)

        self.setObjectName("GachaReportWidget")
        self.initFrame()

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        if utils.getAccountUid() == 0:
            infoBars.warningBar(self.tr("Warning"), self.tr("No account information found"), InfoBarPosition.BOTTOM, self)

    def initFrame(self):
        self.headerLeftGachaReportTitleLabel.setFont(utils.getFont(18))
        self.headerLeftGachaReportTitleLabel.setStyleSheet("color: white;")
        self.headerLeftGachaReportUIDLabel.setStyleSheet("color: grey;")
        self.headerRightFullUpdateDropBtn.setFixedWidth(200)
        self.headerRightFullUpdateDropBtnMenu.addAction(QAction(FluentIcon.ALBUM.icon(), self.tr("Proxy Server Mode")))
        self.headerRightFullUpdateDropBtnMenu.addAction(QAction(FluentIcon.DOCUMENT.icon(), self.tr("Web Cache Mode")))
        self.headerRightFullUpdateDropBtnMenu.addAction(QAction(FluentIcon.ALIGNMENT.icon(), self.tr("URL Mode")))
        self.headerRightFullUpdateDropBtn.setMenu(self.headerRightFullUpdateDropBtnMenu)

        self.bottomLeftGachaTable.setRowCount(60)
        self.bottomLeftGachaTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.bottomLeftGachaTable.resizeColumnsToContents()
        self.bottomLeftGachaTable.setColumnCount(5)
        self.bottomLeftGachaTable.verticalHeader().setHidden(True)
        self.bottomLeftGachaTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.bottomLeftGachaTable.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.bottomLeftGachaTable.setHorizontalHeaderLabels([self.tr("ID"), self.tr("Type"), self.tr("Name"), self.tr("Time"), self.tr("Mode")])

        self.bottomRightBasicLabel.setStyleSheet("color: white;")
        self.bottomRightBasicLabel.setFont(utils.getFont(14))
        self.bottomRightBasicTotalLabel.setStyleSheet("color: white;")
        self.bottomRightBasicTotalLabel.setFont(utils.getFont(12))
        self.bottomRightBasicLevel5TotalLabel.setStyleSheet("color: white;")
        self.bottomRightBasicLevel5TotalLabel.setFont(utils.getFont(10))
        self.bottomRightBasicLevel4TotalLabel.setStyleSheet("color: white;")
        self.bottomRightBasicLevel4TotalLabel.setFont(utils.getFont(10))
        self.bottomRightBasicLevel3TotalLabel.setStyleSheet("color: white;")
        self.bottomRightBasicLevel3TotalLabel.setFont(utils.getFont(10))
        self.bottomRightBasicLevel5TotalTextEdit.setReadOnly(True)
        self.bottomRightBasicLevel4TotalTextEdit.setReadOnly(True)

        self.bottomRightAnalysisLabel.setStyleSheet("color: white;")
        self.bottomRightAnalysisLabel.setFont(utils.getFont(14))
        self.bottomRightWeaponAlertLabel.setStyleSheet("color: white;")
        self.bottomRightWeaponAlertLabel.setFont(utils.getFont(10))
        self.bottomRightWeaponAlertLabel.setVisible(False)
        self.bottomRightAnalysisGuaranteeLabel.setStyleSheet("color: white;")
        self.bottomRightAnalysisGuaranteeLabel.setFont(utils.getFont(10))