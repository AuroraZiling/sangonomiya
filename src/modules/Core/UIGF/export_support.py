import json
import pickle
import time

from ...Scripts.Utils.tools import Tools
from ...constant import UIGF_VERSION_EXPORT

utils = Tools()


class ExportSupport:
    def __init__(self, UID, uigfStandard):
        self.uid = UID
        self.uigfStandard = uigfStandard
        self.dataPath = f"{utils.working_dir}/data/{self.uid}/{self.uid}_data.pickle"

    def UIGFSave(self, dst):
        data = pickle.load(open(self.dataPath, 'rb'))
        if self.uigfStandard == "UIGF(Json) v2.3":
            uigfDict = utils.read_metadata("uigf_dict")
            for eachUnit in data["list"]:
                eachUnit["item_id"] = uigfDict[eachUnit["name"]]
        data["info"]["export_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        data["info"]["export_timestamp"] = int(round(time.time() * 1000))
        data["info"]["export_app"] = "sangonomiya"
        data["info"]["export_app_version"] = utils.app_version
        data["info"]["uigf_version"] = UIGF_VERSION_EXPORT[self.uigfStandard]
        data['info']['uid'] = self.uid
        open(dst, 'w', encoding="utf-8").write(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False))
