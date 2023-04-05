import sys

sys.path.append("..")

from enum import Enum

from qfluentwidgets import getIconColor, Theme, FluentIconBase

from components import OSUtils

utils = OSUtils.OSUtils()


class MyFluentIcon(FluentIconBase, Enum):
    """ Custom icons """

    USER = "User"
    GACHA_REPORT = "GachaReport"
    DATA = "Data"
    ANNOUNCEMENT = "Announcement"
    PLUGIN = "Plugin"
    ABOUT = "About"
    GITHUB = "Github"

    def path(self, theme=Theme.AUTO):
        if theme == Theme.AUTO:
            c = getIconColor()
        else:
            c = "white" if theme == Theme.DARK else "black"

        return f'{utils.workingDir}/assets/icons/{self.value}_{c}.svg'
