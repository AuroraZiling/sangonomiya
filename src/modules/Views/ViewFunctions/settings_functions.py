# coding:utf-8
import logging
import os
import time

import requests
from PySide6.QtCore import Signal, QThread
from ...Scripts.Utils import updater, tools
from ...Scripts.Utils.updater import cleanUpdateZip

utils = tools.Tools()


def delete_all_log():
    logDir = os.listdir(f"{utils.working_dir}/logs")
    for eachLogFile in logDir:
        try:
            os.remove(f"{utils.working_dir}/logs/{eachLogFile}")
        except PermissionError:
            continue
    logging.info("[Settings] All logs deleted")


def delete_all_cache():
    cacheDir = os.listdir(f"{utils.working_dir}/cache")
    for eachCacheFile in cacheDir:
        try:
            os.remove(f"{utils.working_dir}/cache/{eachCacheFile}")
        except PermissionError:
            continue
    logging.info("[Settings] All cache files deleted")


class UpdateThread(QThread):
    trigger = Signal(int, str)

    def __init__(self, info, downloadWay, parent=None):
        super(UpdateThread, self).__init__(parent)
        self.info = info
        self.downloadWay = downloadWay

    def run(self):
        self.trigger.emit(0, f"正在从 {self.downloadWay} 获取更新")
        if "Github" in self.downloadWay:
            try:
                compressed_url = self.info['assets'][0]['browser_download_url']
                file_name = self.info['assets'][0]['name']
            except ConnectionError:
                self.trigger.emit(1, "更新失败")
                return
            except requests.exceptions.SSLError:
                self.trigger.emit(1, "更新失败")
                return
            url = compressed_url
        else:
            url = f"https://sangonomiya-generic.pkg.coding.net/sangonomiya/release/[{self.info['tag_name']}]Sangonomiya.zip"
            file_name = f"Sangonomiya.zip"
        if not os.path.exists('temp'):
            os.mkdir('temp')
        resp = requests.get(url, stream=True)
        count = resp.headers.get('content-length')
        with open(f'temp/{file_name}', 'wb') as f:
            for chunk in resp.iter_content(chunk_size=2048):
                if chunk:
                    f.write(chunk)
                    self.trigger.emit(0, f"正在下载: {f.tell()} 字节/{count} 字节")
        self.trigger.emit(2, "更新下载完毕")


class IsNeedUpdateThread(QThread):
    trigger = Signal(int, object)

    def __init__(self, appVersion, parent=None):
        super(IsNeedUpdateThread, self).__init__(parent)
        self.appVersion = appVersion
        self.newVersion = {}

    def run(self):
        cleanUpdateZip()
        self.newVersion = updater.isNeedUpdate(utils.app_version)
        if self.newVersion is None:
            self.trigger.emit(1, "Sangonomiya 无需更新")
            return
        elif isinstance(self.newVersion, tuple):
            self.trigger.emit(2,
                              f"Sangonomiya 更新请求超过限额\n请于{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(self.newVersion[1]['X-RateLimit-Reset'])))}之后再试")
            return
        self.trigger.emit(0, dict(self.newVersion))
