import json

from requests import get

announce_request_model = "https://hk4e-api-static.mihoyo.com/common/hk4e_cn/announcement/api/getAnnContent?game=hk4e&game_biz=hk4e_cn&lang=zh-cn&bundle_id=hk4e_cn&platform=pc&region=cn_gf01&t=1663409289&level=60&channel_id=1"
up_character_color = {"风": "#00FF00", "岩": "#FFD700", "雷": "#7B68EE", "水": "#00BFFF", "火": "#FF4500",
                      "冰": "#4169E1", "草": "#7CFC00"}


def get_exporter_version(config_path):
    return json.loads(open(config_path, "r", encoding="utf-8").read())["about"]["version"]


class Information:
    def __init__(self):
        self.announce_data = get(announce_request_model).json()["data"]

    def get_up_character(self, with_color=False):
        announce_list = self.announce_data["list"]
        up_list, color_list = [], []
        for announce in announce_list:
            if "概率UP！" in announce["title"] and "神铸赋形" not in announce["title"]:
                up_list.append(announce["title"].split("：")[1].split("概率UP！")[0])
                color_list.append(
                    up_character_color[announce["title"].split("：")[1].split("概率UP！")[0].split("(")[1][0]])
        return up_list if not with_color else (up_list, color_list)

    def get_up_weapon(self):
        announce_list = self.announce_data["list"]
        up_list = []
        for announce in announce_list:
            if "概率UP！" in announce["title"] and "神铸赋形" in announce["title"]:
                up_list.append(announce["title"].split("：")[1].split("概率UP！")[0])
        return up_list
