from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout

from qfluentwidgets import SwitchSettingCard, PushSettingCard, InfoBar, InfoBarPosition
from qfluentwidgets import FluentIcon

from .ViewConfigs.config import cfg
from ..Scripts.Utils import metadata_utils, config_utils, log_recorder as log
from ..Scripts.UI.style_sheet import StyleSheet

utils = config_utils.ConfigUtils()


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

        log.infoWrite("[Settings] All cache files deleted")

    def __metaDataCharacterWeaponUpdateCardClicked(self):
        metadata_utils.updateMetaData("character")
        metadata_utils.updateMetaData("weapon")
        InfoBar.success("成功", "角色/武器元数据列表已更新", position=InfoBarPosition.TOP_RIGHT, parent=self)
        log.infoWrite(f"[Metadata] Character and weapon metadata updated")

    def initFrame(self):
        self.metaDataTitleLabel.setObjectName("metaDataTitleLabel")
        self.metaDataAutoUpdateLabel.setFont(utils.getFont(18))
        self.metaDataCharacterWeaponUpdateLabel.setFont(utils.getFont(18))

        self.metaDataCharacterWeaponUpdateCard.clicked.connect(self.__metaDataCharacterWeaponUpdateCardClicked)
