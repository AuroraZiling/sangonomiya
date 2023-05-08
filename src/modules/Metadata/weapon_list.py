import requests
from lxml import etree

WEAPON_URL = "https://wiki.biligame.com/ys/%E6%AD%A6%E5%99%A8%E5%9B%BE%E9%89%B4"


def categoryWeaponInStar():
    originalData = requests.get(WEAPON_URL).text
    html = etree.HTML(originalData)
    level_5 = []
    level_4 = []
    level_3 = []
    count = 2
    while True:
        try:
            name = html.xpath(f"/html/body/div[2]/div[2]/div[4]/div[5]/div/table[2]/tbody/tr[{count}]/td[2]/a/text()")[
                0]
            level = html.xpath(f"/html/body/div[2]/div[2]/div[4]/div[5]/div/table[2]/tbody/tr[{count}]/td[4]/span/text()")[
                0].replace("\\n", '')
            if level == '3':
                level_3.append(name)
            elif level == '4':
                level_4.append(name)
            elif level == '5':
                level_5.append(name)
            count += 1
        except IndexError:
            break
    return {"5": level_5, "4": level_4, "3": level_3}
