from PySide6 import QtGui, QtWidgets
from PySide6.QtWidgets import QFrame, QLabel, QHBoxLayout, QVBoxLayout

from qfluentwidgets import HyperlinkCard, isDarkTheme, TextEdit, SwitchSettingCard, PushSettingCard
from qfluentwidgets import FluentIcon
from .ViewConfigs.config import cfg

from ..Scripts.UI import customIcon
from ..Scripts.UI.styleSheet import StyleSheet
from ..Scripts.Utils import ConfigUtils
from ..Scripts.Utils import logTracker as log

utils = ConfigUtils.ConfigUtils()


class MetaDataWidget(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.baseVBox = QVBoxLayout(self)

        self.metaDataTitleLabel = QLabel("元数据", self)

        self.metaDataAutoUpdateLabel = QLabel("自动更新", self)

        self.metaDataAutoUpdateCard = SwitchSettingCard(
            FluentIcon.UPDATE,
            "启动时自动更新元数据",
            "",
            configItem=cfg.metaDataUpdateAtStartUp,
            parent=self
        )

        self.metaDataCharacterWeaponUpdateLabel = QLabel("角色/武器", self)

        self.metaDataCharacterWeaponUpdateCard = PushSettingCard(
            "更新",
            FluentIcon.UPDATE,
            "更新角色和武器的元数据列表",
            "",
            parent=self
        )

        self.baseVBox.addWidget(self.metaDataTitleLabel)
        self.baseVBox.addWidget(self.metaDataAutoUpdateLabel)
        self.baseVBox.addWidget(self.metaDataAutoUpdateCard)
        self.baseVBox.addWidget(self.metaDataCharacterWeaponUpdateLabel)
        self.baseVBox.addWidget(self.metaDataCharacterWeaponUpdateCard)
        self.baseVBox.addStretch(1)

        self.setObjectName("MetaDataWidget")
        self.initFrame()
        StyleSheet.METADATA_FRAME.apply(self)

    def initFrame(self):
        self.metaDataTitleLabel.setObjectName("metaDataTitleLabel")
        self.metaDataAutoUpdateLabel.setFont(utils.getFont(18))
        self.metaDataCharacterWeaponUpdateLabel.setFont(utils.getFont(18))
