import os
import pathlib

from ..Utils import log_recorder as log


def create_directory(path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    log.infoWrite(f"[File Verification] Directory {path} created")


def find_directory(path):
    if not os.path.exists(path):
        return False
    return True
