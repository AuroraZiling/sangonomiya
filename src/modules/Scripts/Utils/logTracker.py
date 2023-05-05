import logging
import os.path
import time
from ..Utils.ConfigUtils import ConfigUtils

utils = ConfigUtils()


def debugWrite(content):
    logging.debug(content)


def infoWrite(content):
    logging.info(content)


def warningWrite(content):
    logging.warning(content)


def criticalWrite(content):
    logging.critical(content)


def errorWrite(content):
    logging.error(content)


logDirPath = utils.workingDir + "/logs"
if not os.path.exists(logDirPath):
    os.mkdir(logDirPath)
if utils.getConfigAutoDeleteLog():
    utils.deleteFiles(logDirPath)
logFileName = "Sangonomiya " + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + ".log"
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename=logDirPath+"/"+logFileName,
    filemode='w'
)
