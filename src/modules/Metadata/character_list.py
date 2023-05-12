import requests
from lxml import etree
from ..constant import CHARACTER_URL, PERMANENT_CHARACTER_URL


def getPermanentCharacter():
    return requests.get(PERMANENT_CHARACTER_URL).json()["permanent"]


def categoryCharacterInStar():
    originalData = requests.get(CHARACTER_URL).text
    html = etree.HTML(originalData)
    level_5 = []
    level_4 = []
    count = 2
    while True:
        try:
            name = html.xpath(f"/html/body/div[2]/div[2]/div[4]/div[5]/div/table[2]/tbody/tr[{count}]/td[2]/a/text()")[
                0]
            level = html.xpath(f"/html/body/div[2]/div[2]/div[4]/div[5]/div/table[2]/tbody/tr[{count}]/td[3]/text()")[
                0].replace("\\n", '')
            if "旅行者" not in name:
                if "4" in level:
                    level_4.append(name)
                elif "5" in level:
                    level_5.append(name)
            count += 1
        except IndexError:
            break
    return {"5": level_5, "4": level_4}
