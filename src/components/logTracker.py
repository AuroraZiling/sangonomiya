import logging
import time
from components.OSUtils import getWorkingDir


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


logDirPath = getWorkingDir() + "/logs/"
logFileName = "Sangonomiya " + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + ".log"
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename=logDirPath+"/"+logFileName,
    filemode='w'
)
