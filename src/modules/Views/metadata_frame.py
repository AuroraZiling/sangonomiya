from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout

from qfluentwidgets import SwitchSettingCard, PushSettingCard, InfoBar, InfoBarPosition, IndeterminateProgressBar
from qfluentwidgets import FluentIcon

from .ViewConfigs.config import cfg
from .ViewFunctions.metadataFunctions import MetadataUpdateThread, MetadataUIGFUpdateThread
from ..Scripts.Utils import config_utils, log_recorder as log
from ..Scripts.UI.style_sheet import StyleSheet

utils = config_utils.ConfigUtils()


class MetaDataWidget(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.baseVBox = QVBoxLayout(self)

        self.metaDataTitleLabel = QLabel("元数据", self)
        self.metaDataSubTitleLabel = QLabel("建议在大版本更新后更新", self)

        self.metaDataAutoUpdateLabel = QLabel("自动更新", self)

        self.metaDataAutoUpdateCard = SwitchSettingCard(
            FluentIcon.UPDATE,
            "启动时自动更新元数据",
            "",
            configItem=cfg.metaDataUpdateAtStartUp,
            parent=self
        )

        self.metaDataCharacterWeaponUpdateLabel = QLabel("更新", self)

        self.metaDataUpdateCard = PushSettingCard(
            "更新",
            FluentIcon.UPDATE,
            "更新元数据",
            "",
            parent=self
        )

        self.metaDataUpdateProgressBar = IndeterminateProgressBar(self)

        self.metaDataUIGFUpdateCard = PushSettingCard(
            "更新",
            FluentIcon.UPDATE,
            "更新UIGF API数据",
            "",
            parent=self
        )

        self.metaDataUIGFUpdateProgressBar = IndeterminateProgressBar(self)

        self.baseVBox.addWidget(self.metaDataTitleLabel)
        self.baseVBox.addWidget(self.metaDataSubTitleLabel)
        self.baseVBox.addWidget(self.metaDataAutoUpdateLabel)
        self.baseVBox.addWidget(self.metaDataAutoUpdateCard)
        self.baseVBox.addWidget(self.metaDataCharacterWeaponUpdateLabel)
        self.baseVBox.addWidget(self.metaDataUpdateCard)
        self.baseVBox.addWidget(self.metaDataUpdateProgressBar)
        self.baseVBox.addWidget(self.metaDataUIGFUpdateCard)
        self.baseVBox.addWidget(self.metaDataUIGFUpdateProgressBar)
        self.baseVBox.addStretch(1)

        self.setObjectName("MetaDataWidget")
        self.initFrame()
        StyleSheet.METADATA_FRAME.apply(self)

        log.infoWrite("[Settings] All cache files deleted")

    def __metaDataUpdateCardSignal(self, status):
        if status:
            self.metaDataUpdateCard.setEnabled(True)
            self.metaDataUpdateProgressBar.setVisible(False)
            InfoBar.success("成功", "元数据已更新", position=InfoBarPosition.TOP_RIGHT, parent=self)
            log.infoWrite(f"[Metadata] Character and weapon metadata updated")

    def __metaDataUpdateCardClicked(self):
        self.metaDataUpdateCard.setEnabled(False)
        self.metaDataUpdateProgressBar.setVisible(True)
        self.metaDataUpdateThread = MetadataUpdateThread()
        self.metaDataUpdateThread.start()
        self.metaDataUpdateThread.trigger.connect(self.__metaDataUpdateCardSignal)

    def __metaDataUIGFUpdateCardSignal(self, status):
        message = "UIGF API 数据已更新" if status else "UIGF API 数据无需更新"
        self.metaDataUIGFUpdateCard.setEnabled(True)
        self.metaDataUIGFUpdateProgressBar.setVisible(False)
        InfoBar.success("成功", message, position=InfoBarPosition.TOP_RIGHT, parent=self)
        log.infoWrite(f"[Metadata] UIGF metadata updated")

    def __metaDataUIGFUpdateCardClicked(self):
        self.metaDataUIGFUpdateCard.setEnabled(False)
        self.metaDataUIGFUpdateProgressBar.setVisible(True)
        self.metaDataUIGFUpdateThread = MetadataUIGFUpdateThread()
        self.metaDataUIGFUpdateThread.start()
        self.metaDataUIGFUpdateThread.trigger.connect(self.__metaDataUIGFUpdateCardSignal)

    def initFrame(self):
        self.metaDataTitleLabel.setObjectName("metaDataTitleLabel")
        self.metaDataSubTitleLabel.setObjectName("metaDataSubTitleLabel")
        self.metaDataAutoUpdateLabel.setFont(utils.getFont(18))
        self.metaDataCharacterWeaponUpdateLabel.setFont(utils.getFont(18))

        self.metaDataUpdateProgressBar.setVisible(False)
        self.metaDataUIGFUpdateProgressBar.setVisible(False)

        self.metaDataUpdateCard.clicked.connect(self.__metaDataUpdateCardClicked)
        self.metaDataUIGFUpdateCard.clicked.connect(self.__metaDataUIGFUpdateCardClicked)

        if cfg.metaDataUpdateAtStartUp.value:
            self.__metaDataUpdateCardClicked()
            self.__metaDataUIGFUpdateCardClicked()
