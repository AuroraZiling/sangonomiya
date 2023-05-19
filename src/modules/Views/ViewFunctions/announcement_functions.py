import json
import os
import re
import logging
import requests

from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QListWidgetItem

import requests
from ...Scripts.Utils import downloader, tools
from ...constant import HTML_MODEL

utils = tools.Tools()

def get_announce_data() -> dict:
    if utils.find_exist(f"{utils.working_dir}/cache/announce.json"):
        try:
            return json.loads(open(f"{utils.working_dir}/cache/announce.json", 'r', encoding="utf-8").read())
        except json.decoder.JSONDecodeError:
            return {}
    return {}


def get_announce_icon_data() -> dict:
    try:
        return json.loads(open(f"{utils.working_dir}/cache/announce_icons.json", 'r', encoding="utf-8").read())
    except json.decoder.JSONDecodeError:
        return {}


def getImageURLFromSource(source):
    pattern = re.compile(r'https://webstatic.mihoyo.com/upload/ann/[^\s]+.jpg')
    url_lst = pattern.findall(source)
    logging.info("[Announcement] Inner image URLs extracted")
    return url_lst


def contentHTMLPhaser(css, contentHTML, innerImageUrl=None):
    contentHTML = contentHTML.replace('''style="color:rgba(85,85,85,1)"''', "")
    contentHTML = contentHTML.replace('''style="background-color: rgb(255, 215, 185);"''', "")
    contentHTML = contentHTML.replace('''style="background-color: rgb(254, 245, 231);"''', "")
    contentHTML = contentHTML.replace('''&lt;t class="t_lc"&gt;''', "")
    contentHTML = contentHTML.replace('''&lt;t class="t_gl"&gt;''', "")
    contentHTML = contentHTML.replace('''&lt;/t&gt;''', "")
    contentHTML = HTML_MODEL.replace("{css}", css).replace("{content}", contentHTML)
    if innerImageUrl:
        for eachInnerImage in innerImageUrl.keys():
            contentHTML = contentHTML.replace(eachInnerImage, innerImageUrl[eachInnerImage])
    logging.info("[Announcement][contentHTMLPhaser] HTML Generated")
    return contentHTML


class AnnouncementFunctions:
    def __init__(self, announceData, announceIconData):
        self.announceData = announceData["data"]
        self.announceIconData = announceIconData["data"]["list"]
        self.announceAmount = self.announceData["total"]
        self.announceIconURLList = []
        self.announceIconNameList = []
        self.announceTitleList = []
        self.announceInnerImageMapping = {}

        self.announceStyle = open(f"{utils.working_dir}/assets/css/github-markdown-light.css", 'r').read()

        self.getIconsURL()
        self.getTitles()

    def getIconsURL(self):
        for first_level in self.announceIconData:
            for second_level in first_level["list"]:
                self.announceIconURLList.append(second_level["tag_icon"])
                self.announceIconNameList.append(second_level["tag_icon"].split("/")[-1])
        logging.info("[Announcement] Icon URLs of announcement got")

    def getIcons(self):
        for eachIconURL in self.announceIconURLList:
            if not os.path.exists(f"{utils.working_dir}/cache/{eachIconURL.split('/')[-1]}"):
                downloader.downloadFromImage(eachIconURL, f"{utils.working_dir}/cache/", eachIconURL.split('/')[-1])
            else:
                pass
        logging.info("[Announcement] Icons of announcement downloaded")

    def getTitles(self):
        for eachAnnounce in self.announceData["list"]:
            self.announceTitleList.append(eachAnnounce["subtitle"].replace("<br>", ""))
        logging.info("[Announcement] Titles of announcement got")

    def getItems(self):
        sideBarItems = []
        for eachItem in range(self.announceAmount):
            sideBarItems.append(
                QListWidgetItem(QIcon(f"{utils.working_dir}/cache/{self.announceIconNameList[eachItem]}"),
                                self.announceTitleList[eachItem]))
        return sideBarItems

    def getCurrentAnnounce(self, index):
        currentAnnounce = self.announceData["list"][index]
        announceId = str(currentAnnounce["ann_id"])
        bigTitle = currentAnnounce["title"]
        contentHtml = currentAnnounce["content"]
        innerImageSources = getImageURLFromSource(contentHtml)
        for eachInnerImage in innerImageSources:
            if not os.path.exists(f"{utils.working_dir}/cache/{eachInnerImage.split('/')[-1]}"):
                downloader.downloadFromImage(eachInnerImage, f"{utils.working_dir}/cache/",
                                             eachInnerImage.split('/')[-1])
                self.announceInnerImageMapping[
                    eachInnerImage] = f"{utils.working_dir}/cache/{eachInnerImage.split('/')[-1]}"
        if currentAnnounce["banner"]:
            downloader.downloadFromImage(currentAnnounce["banner"], f"{utils.working_dir}/cache/",
                                         announceId + ".jpg") if not os.path.exists(
                f"{utils.working_dir}/cache/{announceId}.jpg") else None
            banner = QPixmap(f"{utils.working_dir}/cache/{announceId}.jpg")
            bannerSize = banner.rect().getRect()
            if banner.rect().getRect() == (0, 0, 0, 0):
                os.remove(f"{utils.working_dir}/cache/{announceId}.jpg")
                try:
                    downloader.downloadFromImage(currentAnnounce["banner"], f"{utils.working_dir}/cache/",
                                                 announceId + ".jpg")
                except requests.exceptions.MissingSchema:
                    pass
                banner = QPixmap(f"{utils.working_dir}/cache/{announceId}.jpg")
            bannerHeight = round(750 / bannerSize[2] * bannerSize[3])
        else:
            banner = ""
            bannerHeight = 0
        contentHtml = contentHTMLPhaser(self.announceStyle, contentHtml, self.announceInnerImageMapping)
        open(f"{utils.working_dir}/cache/{index}.html", 'w', encoding="utf-8").write(contentHtml)
        data = {"announceId": announceId, "bigTitle": bigTitle, "banner": banner, "bannerHeight": bannerHeight,
                "contentHtml": f"{index}.html"}
        logging.info(f"[Announcement] Current announcement: {data}")
        return data
