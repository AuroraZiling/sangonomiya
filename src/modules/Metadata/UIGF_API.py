import hashlib
import os
from functools import partial

import requests
import json

from ..constant import UIGF_ITEM_ID_URL, UIGF_MD5_URL
from ..Scripts.Utils.tools import Tools

utils = Tools()


def updateUIGFItemIdList(language, localPath):
    if not os.path.exists(f"{utils.config_dir}/metadata/"):
        os.mkdir(f"{utils.config_dir}/metadata/")
    if not os.path.exists(localPath):
        with open(localPath, 'wb') as f:
            data = getUIGFItemIdList(language)
            if data:
                text = json.dumps(data, indent=4, ensure_ascii=False).replace('\r\n', '\n')
                f.write(text.encode('utf-8'))
                return True
            else:
                return False
    with open(localPath, 'rb') as f:
        d = hashlib.md5()
        for buf in iter(partial(f.read, 1024), b''):
            d.update(buf)
    local_md5 = d.hexdigest()
    try:
        api_md5 = requests.get(UIGF_MD5_URL).json()["chs"]
    except requests.exceptions.ConnectTimeout:
        return False
    if not local_md5 == api_md5:
        with open(localPath, 'wb') as f:
            data = getUIGFItemIdList(language)
            if data:
                text = json.dumps(getUIGFItemIdList(language), indent=4, ensure_ascii=False).replace('\r\n', '\n')
                f.write(text.encode('utf-8'))
                return True
            else:
                return False


def getUIGFItemIdList(language):
    try:
        return requests.get(UIGF_ITEM_ID_URL.format(lang=language)).json()
    except requests.exceptions.ConnectTimeout:
        return {}