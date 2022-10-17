import json
import os.path

import requests
from PyQt6 import QtCore
from PyQt6.QtGui import QFont, QPixmap, QFontDatabase, QIcon
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QListWidget, QListWidgetItem

request_model = "https://hk4e-api-static.mihoyo.com/common/hk4e_cn/announcement/api/getAnnContent?game=hk4e&game_biz=hk4e_cn&lang=zh-cn&bundle_id=hk4e_cn&platform=pc&region=cn_gf01&t=1663409289&level=60&channel_id=1"
icon_model = "https://hk4e-api.mihoyo.com/common/hk4e_cn/announcement/api/getAnnList?game=hk4e&game_biz=hk4e_cn&lang=zh-cn&auth_appid=announcement&authkey_ver=1&bundle_id=hk4e_cn&channel_id=1&level=60&platform=pc&region=cn_gf01&sdk_presentation_style=fullscreen&sdk_screen_transparent=true&sign_type=2&uid=1"
html_model = '''
<!DOCTYPE html>
<html>
  <head>
  <body style="background-color:#FAEBD7;"></body>
  </head>
  <body>
    {content}
  </body>
</html>
'''


class Announce(QWidget):
    def __init__(self):
        super(Announce, self).__init__()
        self.source = {}
        self.icon_list = []
        self.setWindowTitle("公告 / Announce")
        self.setFixedSize(1050, 600)
        self.base_layout = QHBoxLayout(self)
        self.global_font = "Microsoft YaHei"

        # Sidebar
        self.side_bar = QListWidget()
        self.base_layout.addWidget(self.side_bar)

        # Content
        self.content_v_layout = QVBoxLayout()
        self.content_title = QLabel()
        self.banner = QLabel()
        self.content = QWebEngineView()
        self.content_v_layout.addWidget(self.content_title)
        self.content_v_layout.addWidget(self.banner)
        self.content_v_layout.addWidget(self.content)

        self.base_layout.addLayout(self.content_v_layout)

        self.setLayout(self.base_layout)

        self.get_announce()
        self.initUI()

    def get_announce(self):
        try:
            self.source = requests.get(request_model).json()["data"]
            open("cache/announce.json", "w", encoding="utf-8").write(
                json.dumps(self.source, indent=4, ensure_ascii=False))
        except requests.exceptions.ConnectionError:
            pass

    def initUI(self):
        # Font
        if os.path.exists("assets/font.ttf"):
            self.global_font = QFontDatabase.applicationFontFamilies(
                QFontDatabase.addApplicationFont("assets/font.ttf"))
        # Sidebar
        self.side_bar.setFixedWidth(350)
        self.side_bar.minimumSizeHint()
        self.get_icon_list()
        for each in range(self.source["total"]):
            if not os.path.exists(f"cache/{self.icon_list[each].split('/')[-1]}"):
                open(f"cache/{self.icon_list[each].split('/')[-1]}", "wb").write(
                    requests.get(self.icon_list[each]).content)
            subtitle = self.source["list"][each]["subtitle"].replace("<br>", "")
            self.side_bar.addItem(QListWidgetItem(QIcon(f"cache/{self.icon_list[each].split('/')[-1]}"), subtitle))
            self.side_bar.item(each).setSizeHint(QtCore.QSize(300, 30))
            self.side_bar.item(each).setFont(QFont("Microsoft YaHei", 10))
        self.side_bar.itemClicked.connect(self.update_content)
        # Content
        self.content_title.setFont(QFont(self.global_font, 16))
        self.banner.setFixedSize(674, 236)
        self.banner.setScaledContents(True)
        self.content.hide()

    def get_icon_list(self):
        for first_level in requests.get(icon_model).json()["data"]["list"]:
            for second_level in first_level["list"]:
                self.icon_list.append(second_level["tag_icon"])

    def update_content(self):
        self.content.show()
        # Title
        self.content_title.setText(self.source["list"][self.side_bar.currentRow()]["title"])
        # Banner
        self.banner.setFixedSize(674, 236)
        self.content.setFixedHeight(300)
        announce_id = self.source['list'][self.side_bar.currentRow()]['ann_id']
        if not self.source["list"][self.side_bar.currentRow()]["banner"]:
            self.banner.hide()
            self.content.setFixedHeight(550)
        else:
            self.banner.show()
            self.content.setFixedHeight(300)
        if "祈愿" in self.side_bar.currentItem().text():
            self.banner.setFixedSize(674, 326)
            self.content.setFixedHeight(210)
        if not os.path.exists(f"cache/{announce_id}.jpg"):
            try:
                open(f"cache/{announce_id}.jpg", "wb").write(
                    requests.get(self.source["list"][self.side_bar.currentRow()]["banner"]).content)
            except requests.exceptions.MissingSchema:
                pass
        self.banner.setPixmap(QPixmap(f"cache/{announce_id}.jpg"))
        self.html_generator(self.source["list"][self.side_bar.currentRow()]["content"])

    def html_generator(self, content):
        # 这个地方最好用正则，但是我不会捏！这里的大坑，以后再来填吧！
        content = content.replace("<img src=", "<img width=645 src=")
        content = content.replace("0.1rem", "1rem")
        content = content.replace("0.10rem", "1rem")
        content = content.replace("0.12rem", "1rem")
        content = content.replace("line-height: 2", "line-height: 1.5")
        content = content.replace("min-height: 1.5em;", "min-height: 1em;")
        content = content.replace("white-space: pre-wrap;", "")
        content = content.replace('''&lt;t class="t_lc"&gt;''', "")
        content = content.replace('''&lt;t class="t_gl"&gt;''', "")
        content = content.replace('''&lt;/t&gt;''', "")
        content = content.replace('''javascript:miHoYoGameJSSDK.openInWebview(\'''', "")
        content = content.replace("')", "")
        self.content.setHtml(html_model.replace("{content}", content))
