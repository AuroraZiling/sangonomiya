import sys

sys.path.append("..")

from enum import Enum

from qfluentwidgets import getIconColor, Theme, FluentIconBase

from components import OSUtils

WORKING_DIR = OSUtils.getWorkingDir()


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

        return f'{WORKING_DIR}/assets/icons/{self.value}_{c}.svg'
