from PySide6.QtCore import Qt, Signal, QEvent
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QFrame

from qfluentwidgets import MessageBox, TextEdit, PrimaryPushButton, TextWrap, FluentStyleSheet, ComboBox, PushButton, \
    InfoBar
from qfluentwidgets.components.dialog_box.dialog import Dialog, Ui_MessageBox

from qfluentwidgets.components.dialog_box.mask_dialog_base import MaskDialogBase

from ..Utils.tools import Tools
from ...Core.GachaReport.gachaReportUtils import extractAPI

utils = Tools()


class URLDialog(MaskDialogBase, Ui_MessageBox):
    """ Message box """

    returnSignal = Signal(str)
    cancelSignal = Signal()

    def __init__(self, title: str, content: str, parent=None):
        super().__init__(parent=parent)
        self._setUpUi(title, content, self.widget)

        self.setShadowEffect(60, (0, 10), QColor(0, 0, 0, 50))
        self.setMaskColor(QColor(0, 0, 0, 76))
        self._hBoxLayout.removeWidget(self.widget)
        self._hBoxLayout.addWidget(self.widget, 1, Qt.AlignmentFlag.AlignCenter)

        self.textEditWidget = TextEdit(self)
        self.textEditWidget.setFixedWidth(500)
        self.vBoxLayout.insertWidget(1, self.textEditWidget)

        self.getFromClipboardBtn = PushButton("从剪贴板获取", self.buttonGroup)
        self.buttonLayout.insertWidget(1, self.getFromClipboardBtn)

        self.buttonGroup.setMinimumWidth(280)
        self.widget.setFixedSize(500, 350)

        self.yesButton.clicked.connect(self.__yesButtonClicked)
        self.getFromClipboardBtn.clicked.connect(self.__getFromClipboardBtnClicked)

    def __getFromClipboardBtnClicked(self):
        clipboardText = extractAPI(utils.getClipboardText())
        if clipboardText:
            self.textEditWidget.setText(clipboardText)

    def __yesButtonClicked(self):
        self.accept()
        self.returnSignal.emit(self.textEditWidget.toPlainText())