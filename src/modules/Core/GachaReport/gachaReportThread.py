import json
import os
import pathlib
import pickle
import time

import requests
from PyQt6.QtCore import QThread, pyqtSignal
from ..UIGF.support import UIGF_VERSION, UIGF_GACHATYPE, UIGF_DATA_MODEL, GACHATYPE
from ..UIGF.converter import originalToUIGFListUnit
from .gachaReportUtils import updateAPI
from ...Scripts.Utils.ConfigUtils import ConfigUtils

utils = ConfigUtils()
gachaTarget = ""


class GachaReportThread(QThread):
    trigger = pyqtSignal(tuple)

    def __init__(self, gachaUrl, parent=None):
        super(GachaReportThread, self).__init__(parent)
        self.uid = ""
        self.gachaUrl = gachaUrl

    def run(self):
        UIGFExportJsonData = UIGF_DATA_MODEL
        gachaList = []
        for key in GACHATYPE.keys():
            end_id = "0"
            page = 0
            if key == "新手祈愿":
                continue
            while True:
                apiPerUnit = updateAPI(self.gachaUrl, GACHATYPE[key], 20, page, end_id)
                responsePerUnit = json.loads(requests.get(apiPerUnit).content.decode("utf-8"))
                gachaPerResponse = responsePerUnit["data"]["list"]
                if not len(gachaPerResponse):
                    break
                self.uid = responsePerUnit['data']["list"][0]['uid']
                self.trigger.emit((0, f"{self.tr('Fetching: ')}{str(page)} | {self.tr('Gacha type: ')}{key}"))
                for i in gachaPerResponse:
                    gachaList.append(originalToUIGFListUnit(i, UIGF_GACHATYPE[GACHATYPE[key]]))
                end_id = responsePerUnit["data"]["list"][-1]["id"]
                page += 1
                self.usleep(500)
        pathlib.Path(f"{utils.workingDir}/data/{self.uid}").mkdir(parents=True, exist_ok=True)
        UIGFExportJsonData["info"]["export_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        UIGFExportJsonData["info"]["export_timestamp"] = int(round(time.time() * 1000))
        UIGFExportJsonData["info"]["export_app"] = "sangonomiya"
        UIGFExportJsonData["info"]["export_app_version"] = utils.appVersion
        UIGFExportJsonData["info"]["uigf_version"] = UIGF_VERSION
        UIGFExportJsonData['info']['uid'] = self.uid
        UIGFExportJsonData["list"] = gachaList
        open(f"{utils.workingDir}/data/{self.uid}/{self.uid}_export_data.json", "w", encoding="utf-8").write(
            json.dumps(UIGFExportJsonData, indent=2, sort_keys=True, ensure_ascii=False))
        with open(f"{utils.workingDir}/data/{self.uid}/{self.uid}_data.pickle", 'wb') as f:
            pickle.dump(UIGFExportJsonData, f)
        self.trigger.emit((1, self.tr("GachaLog Update Completed")))
