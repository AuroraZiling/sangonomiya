import os
from enum import Enum

from qfluentwidgets import getIconColor, Theme, FluentIconBase


class MyFluentIcon(FluentIconBase, Enum):
    """ Custom icons """

    USER = "User"
    GACHA_REPORT = "GachaReport"
    ANNOUNCEMENT = "Announcement"
    PLUGIN = "Plugin"

    def path(self, theme=Theme.AUTO):
        if theme == Theme.AUTO:
            c = getIconColor()
        else:
            c = "white" if theme == Theme.DARK else "black"

        return f'./assets/icons/{self.value}_{c}.svg'
