import os
import sys

from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QListWidgetItem

sys.path.append("..")

import json
import requests
from components import infoBars, downloader
from components.OSUtils import getWorkingDir, HTML_MODEL


def contentHTMLPhaser(contentHTML):
    contentHTML = contentHTML.replace("0.1rem", "1rem")
    contentHTML = contentHTML.replace("0.10rem", "1rem")
    contentHTML = contentHTML.replace("0.12rem", "1rem")
    contentHTML = contentHTML.replace("line-height: 2", "line-height: 1.5")
    contentHTML = contentHTML.replace("min-height: 1.5em;", "min-height: 1em;")
    contentHTML = contentHTML.replace("white-space: pre-wrap;", "")
    contentHTML = contentHTML.replace('''&lt;t class="t_lc"&gt;''', "")
    contentHTML = contentHTML.replace('''&lt;t class="t_gl"&gt;''', "")
    contentHTML = contentHTML.replace('''&lt;/t&gt;''', "")
    contentHTML = contentHTML.replace('''javascript:miHoYoGameJSSDK.openInWebview(\'''', "")
    contentHTML = contentHTML.replace("')", "")
    contentHTML = contentHTML.replace('''<p style="">''', '''<p style="color: white;">''')
    contentHTML = contentHTML.replace("href=\"h", '')
    contentHTML = contentHTML.replace("<span ", "<p ").replace("</span>", "</p>")
    contentHTML = contentHTML.replace("<strong>", "").replace("<,strong>", "")
    contentHTML = contentHTML.replace("rgba(51,51,51,1)", "rgba(220,220,220,1)")
    contentHTML = contentHTML.replace("rgba(65,70,75,1)", "rgba(220,220,220,1)")
    contentHTML = contentHTML.replace("rgba(85,85,85,1)", "rgba(220,220,220,1)")
    contentHTML = contentHTML.replace("rgba(236,73,35,1)", "rgba(220,220,220,1)")
    return HTML_MODEL.replace("{content}", contentHTML)


class AnnouncementFunctions:
    def __init__(self, announceData, announceIconData):
        self.announceData = announceData["data"]
        self.announceIconData = announceIconData["data"]["list"]
        self.announceAmount = self.announceData["total"]
        self.announceIconURLList = []
        self.announceIconNameList = []
        self.announceTitleList = []

        self.getIconsURL()
        self.getTitles()

    def getIconsURL(self):
        try:
            for first_level in self.announceIconData:
                for second_level in first_level["list"]:
                    self.announceIconURLList.append(second_level["tag_icon"])
                    self.announceIconNameList.append(second_level["tag_icon"].split("/")[-1])
        except requests.exceptions.ConnectionError:
            return "ConnectionError"

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

    def getCurrentAnnounce(self, index):
        currentAnnounce = self.announceData["list"][index]
        announceId = str(currentAnnounce["ann_id"])
        bigTitle = currentAnnounce["title"]
        contentHtml = currentAnnounce["content"]
        if not os.path.exists(f"{getWorkingDir()}/cache/{announceId}.jpg"):
            downloader.downloadFromImage(currentAnnounce["banner"], f"{getWorkingDir()}/cache/", announceId + ".jpg")
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
        contentHtml = contentHTMLPhaser(contentHtml)
        return {"announceId": announceId, "bigTitle": bigTitle, "banner": banner, "bannerHeight": bannerHeight,
                "contentHtml": contentHtml}
