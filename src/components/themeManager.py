import sys

sys.path.append("..")

from components import OSUtils

WORKING_DIR = OSUtils.getWorkingDir()


def setTheme(theme):
    return open(f"{WORKING_DIR}/assets/themes/{theme}.qss", encoding='utf-8').read()