import sys

sys.path.append("..")

from components import OSUtils

utils = OSUtils.OSUtils()


def setTheme(theme):
    return open(f"{utils.workingDir}/assets/themes/{theme}.qss", encoding='utf-8').read()