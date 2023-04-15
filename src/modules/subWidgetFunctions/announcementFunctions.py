import os
import re
import sys

from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QListWidgetItem

sys.path.append("..")

import requests
from components import infoBars, downloader
from components.OSUtils import getWorkingDir, HTML_MODEL


def contentHTMLPhaser(css, contentHTML):
    contentHTML = contentHTML.replace('''style="color:rgba(85,85,85,1)"''', "")
    contentHTML = contentHTML.replace('''style="background-color: rgb(255, 215, 185);"''', "")
    contentHTML = contentHTML.replace('''style="background-color: rgb(254, 245, 231);"''', "")
    contentHTML = contentHTML.replace('''&lt;t class="t_lc"&gt;''', "")
    contentHTML = contentHTML.replace('''&lt;t class="t_gl"&gt;''', "")
    contentHTML = contentHTML.replace('''&lt;/t&gt;''', "")
    return HTML_MODEL.replace("{css}", css).replace("{content}", contentHTML)


class AnnouncementFunctions:
    def __init__(self, announceData, announceIconData):
        self.announceData = announceData["data"]
        self.announceIconData = announceIconData["data"]["list"]
        self.announceAmount = self.announceData["total"]
        self.announceIconURLList = []
        self.announceIconNameList = []
        self.announceTitleList = []

        self.announceStyle = open(f"{getWorkingDir()}/assets/css/github-markdown-dark.css", 'r').read()

        self.getIconsURL()
        self.getTitles()

    def getIconsURL(self):
        for first_level in self.announceIconData:
            for second_level in first_level["list"]:
                self.announceIconURLList.append(second_level["tag_icon"])
                self.announceIconNameList.append(second_level["tag_icon"].split("/")[-1])

    def getIcons(self):
        for eachIconURL in self.announceIconURLList:
            if not os.path.exists(f"{getWorkingDir()}/cache/{eachIconURL.split('/')[-1]}"):
                downloader.downloadFromImage(eachIconURL, f"{getWorkingDir()}/cache/", eachIconURL.split('/')[-1])
            else:
                pass

    def getTitles(self):
        for eachAnnounce in self.announceData["list"]:
            self.announceTitleList.append(eachAnnounce["subtitle"].replace("<br>", ""))

    def getItems(self):
        sideBarItems = []
        for eachItem in range(self.announceAmount):
            sideBarItems.append(QListWidgetItem(QIcon(f"{getWorkingDir()}/cache/{self.announceIconNameList[eachItem]}"),
                                                self.announceTitleList[eachItem]))
        return sideBarItems

    def getImageURLFromSource(self, source):
        pattern = re.compile(r'https://webstatic.mihoyo.com/upload/ann/[^\s]+.jpg')
        url_lst = pattern.findall(source)
        return url_lst

    def getCurrentAnnounce(self, index):
        currentAnnounce = self.announceData["list"][index]
        announceId = str(currentAnnounce["ann_id"])
        bigTitle = currentAnnounce["title"]
        contentHtml = currentAnnounce["content"]
        if currentAnnounce["banner"]:
            downloader.downloadFromImage(currentAnnounce["banner"], f"{getWorkingDir()}/cache/", announceId + ".jpg") if not os.path.exists(f"{getWorkingDir()}/cache/{announceId}.jpg") else None
            banner = QPixmap(f"{getWorkingDir()}/cache/{announceId}.jpg")
            bannerSize = banner.rect().getRect()
            if banner.rect().getRect() == (0, 0, 0, 0):
                os.remove(f"{getWorkingDir()}/cache/{announceId}.jpg")
                try:
                    downloader.downloadFromImage(currentAnnounce["banner"], f"{getWorkingDir()}/cache/",
                                                 announceId + ".jpg")
                except requests.exceptions.MissingSchema:
                    pass
                banner = QPixmap(f"{getWorkingDir()}/cache/{announceId}.jpg")
            bannerHeight = round(750 / bannerSize[2] * bannerSize[3])
        else:
            banner = ""
            bannerHeight = 0

        contentHtml = contentHTMLPhaser(self.announceStyle, contentHtml)
        return {"announceId": announceId, "bigTitle": bigTitle, "banner": banner, "bannerHeight": bannerHeight,
                "contentHtml": contentHtml}
