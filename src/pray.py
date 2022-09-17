# -*- coding:utf-8 -*-
import json
import os
import pickle
import subprocess
import sys
import time
import qdarkstyle
import requests
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QBrush, QColor, QFontDatabase
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtWidgets import QWidget, QMainWindow, QHBoxLayout, QTableWidget, QPushButton, QApplication, QVBoxLayout, \
    QMessageBox, QAbstractItemView, QHeaderView, QLabel, QFrame, QTextEdit, QTableWidgetItem

from modules import about_widget
from modules import analysis
from modules import settings_widget
from modules import announce_widget

gachaUrl = ""
gachaType = {"新手祈愿": "100", "常驻祈愿": "200", "角色活动祈愿": "301", "角色活动祈愿-2": "400", "武器祈愿": "302"}
uigfGachaType = {"100": "100", "200": "200", "301": "301", "400": "301", "302": "302"}
gachaTarget = ""
gachaItemLevelColor = {4: QColor(132, 112, 255), 5: QColor(255, 185, 15)}
export_data = {"info": {"uid": "", "lang": "zh-cn", "export_time": ""}, "list": []}

basedir = os.path.dirname(__file__)
hide_new = json.loads(open("config.json", "r", encoding="utf-8").read())["settings"]["hide_new"]

try:
    from ctypes import windll  # Only Windows.

    myAppId = 'AuroraZiling.GPE.GPE.1'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myAppId)
except ImportError:
    pass


class MainForm(QMainWindow):
    def __init__(self):
        super(MainForm, self).__init__()
        self.target_uid = ""
        self.all_data_list = {}
        self.setWindowTitle("Genshin Pray Export")
        self.setFixedSize(1300, 700)
        self.global_font = "Microsoft YaHei"

        # Child Windows
        self.announce_window = announce_widget.Announce()
        self.about_window = about_widget.About()
        self.settings_window = settings_widget.Settings()

        # Pray List Init
        self.loaded_pray_list = []
        self.pray_list = {"100": None, "200": None, "301": None, "400": None, "302": None}

        # Multi-process
        self.get_pray_list_thread = LeftPrayListThread()

        # UI Design
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.base_layout = QVBoxLayout(self)
        self.uid_h_layout = QHBoxLayout(self)
        self.all_layout = QHBoxLayout(self)
        self.left_layout = QVBoxLayout(self)
        self.right_layout = QVBoxLayout(self)

        # UI UID
        self.uid_user_image = QSvgWidget("assets/user.svg")
        self.uid_current_uid_label = QLabel("未知")
        self.uid_announce_btn = QPushButton("游戏公告")
        self.uid_settings_btn = QPushButton("设置")
        self.uid_about_btn = QPushButton("关于")
        self.uid_h_layout.addWidget(self.uid_user_image)
        self.uid_h_layout.addWidget(self.uid_current_uid_label)
        self.uid_h_layout.addWidget(self.uid_announce_btn)
        self.uid_h_layout.addStretch()
        self.uid_h_layout.addWidget(self.uid_settings_btn)
        self.uid_h_layout.addWidget(self.uid_about_btn)
        self.uid_splitter = QFrame(self)
        self.base_layout.addLayout(self.uid_h_layout)
        self.base_layout.addWidget(self.uid_splitter)

        # UI Left
        self.left_top_layout = QHBoxLayout(self)
        self.left_list_label = QLabel("祈愿记录")
        self.left_open_export_dir_btn = QPushButton("打开导出目录")
        self.left_refresh_btn = QPushButton("更新数据")
        self.left_top_layout.addWidget(self.left_list_label)
        self.left_top_layout.addWidget(self.left_open_export_dir_btn)
        self.left_top_layout.addWidget(self.left_refresh_btn)
        self.left_layout.addLayout(self.left_top_layout)

        self.left_pray_list = QTableWidget(self)
        self.left_layout.addWidget(self.left_pray_list)

        self.left_pray_mode_h_layout = QHBoxLayout(self)
        if not hide_new:
            self.left_pray_mode_100_btn = QPushButton("新手祈愿")
            self.left_pray_mode_h_layout.addWidget(self.left_pray_mode_100_btn)
        self.left_pray_mode_200_btn = QPushButton("常驻祈愿")
        self.left_pray_mode_301_btn = QPushButton("角色祈愿")
        # 疑似无用
        # self.left_pray_mode_400_btn = QPushButton("角色祈愿-2")
        self.left_pray_mode_302_btn = QPushButton("武器祈愿")
        self.left_pray_mode_h_layout.addWidget(self.left_pray_mode_200_btn)
        self.left_pray_mode_h_layout.addWidget(self.left_pray_mode_301_btn)
        # self.left_pray_mode_h_layout.addWidget(self.left_pray_mode_400_btn)
        self.left_pray_mode_h_layout.addWidget(self.left_pray_mode_302_btn)
        self.left_layout.addLayout(self.left_pray_mode_h_layout)

        self.left_bottom_h_layout = QHBoxLayout(self)
        self.left_update_time_label = QLabel("数据时间: 未知")
        self.left_status_label = QLabel("状态: 无")
        self.left_bottom_h_layout.addWidget(self.left_update_time_label)
        self.left_bottom_h_layout.addWidget(self.left_status_label)
        self.left_layout.addLayout(self.left_bottom_h_layout)

        # UI Splitter
        self.splitter = QFrame(self)

        # UI Right
        self.right_top_layout = QHBoxLayout(self)
        self.right_label = QLabel("分析")
        self.right_top_layout.addWidget(self.right_label)

        self.right_analysis_layout = QVBoxLayout(self)

        self.right_analysis_basic_label = QLabel("基本数据")
        self.right_analysis_basic_total_label = QLabel("祈愿数: 未知")
        self.right_analysis_basic_5_label = QLabel("5星数量: 未知")
        self.right_analysis_basic_5_list_textEdit = QTextEdit()
        self.right_analysis_basic_4_label = QLabel("4星数量: 未知")
        self.right_analysis_basic_4_list_textEdit = QTextEdit()
        self.right_analysis_basic_3_label = QLabel("3星数量: 未知")
        self.right_analysis_layout.addWidget(self.right_analysis_basic_label)
        self.right_analysis_layout.addWidget(self.right_analysis_basic_total_label)
        self.right_analysis_layout.addWidget(self.right_analysis_basic_5_label)
        self.right_analysis_layout.addWidget(self.right_analysis_basic_5_list_textEdit)
        self.right_analysis_layout.addWidget(self.right_analysis_basic_4_label)
        self.right_analysis_layout.addWidget(self.right_analysis_basic_4_list_textEdit)
        self.right_analysis_layout.addWidget(self.right_analysis_basic_3_label)

        self.right_analysis_right_label = QLabel("保底数据")
        self.right_analysis_right_weapon_alert_label = QLabel("注意: 无法做到针对神铸的分析")
        self.right_analysis_right_guarantee_label = QLabel("暂无")
        self.right_analysis_layout.addWidget(self.right_analysis_right_label)
        self.right_analysis_layout.addWidget(self.right_analysis_right_weapon_alert_label)
        self.right_analysis_layout.addWidget(self.right_analysis_right_guarantee_label)

        self.right_layout.addLayout(self.right_top_layout)
        self.right_layout.addLayout(self.right_analysis_layout)
        self.right_layout.addStretch(1)

        self.all_layout.addLayout(self.left_layout)
        self.all_layout.addWidget(self.splitter)
        self.all_layout.addLayout(self.right_layout)
        self.base_layout.addLayout(self.all_layout)
        self.widget.setLayout(self.base_layout)

        # Functions
        self.file_check()
        self.pre_generate()
        self.initUI()
        self.debug_code()

    def pre_generate(self):
        for each_dir in os.listdir("pray_history"):
            self.all_data_list.update({each_dir: {"data_100": {"data": [], "data_time": ""},
                                                  "data_200": {"data": [], "data_time": ""},
                                                  "data_301": {"data": [], "data_time": ""},
                                                  "data_400": {"data": [], "data_time": ""},
                                                  "data_302": {"data": [], "data_time": ""}}})
            if os.path.exists(f"pray_history/{each_dir}/original_data/100.pickle") and not hide_new:
                data_100 = pickle.load(open(f"pray_history/{each_dir}/original_data/100.pickle", "rb"))
                data_time_100 = time.strftime("%Y-%m-%d %H:%M:%S",
                                              time.localtime((os.path.getmtime(f"pray_history/{each_dir}/original_data/100.pickle"))))
                self.all_data_list[each_dir]["data_100"]["data"] = data_100
                self.loaded_pray_list.append("新手祈愿")
                self.pray_list["100"] = data_100
                self.all_data_list[each_dir]["data_100"]["data_time"] = data_time_100
            if os.path.exists(f"pray_history/{each_dir}/original_data/200.pickle"):
                data_200 = pickle.load(open(f"pray_history/{each_dir}/original_data/200.pickle", "rb"))
                data_time_200 = time.strftime("%Y-%m-%d %H:%M:%S",
                                              time.localtime((os.path.getmtime(f"pray_history/{each_dir}/original_data/200.pickle"))))
                self.all_data_list[each_dir]["data_200"]["data"] = data_200
                self.loaded_pray_list.append("常驻祈愿")
                self.pray_list["200"] = data_200
                self.all_data_list[each_dir]["data_200"]["data_time"] = data_time_200
            if os.path.exists(f"pray_history/{each_dir}/original_data/301.pickle"):
                data_301 = pickle.load(open(f"pray_history/{each_dir}/original_data/301.pickle", "rb"))
                data_time_301 = time.strftime("%Y-%m-%d %H:%M:%S",
                                              time.localtime((os.path.getmtime(f"pray_history/{each_dir}/original_data/301.pickle"))))
                self.all_data_list[each_dir]["data_301"]["data"] = data_301
                self.loaded_pray_list.append("角色祈愿")
                self.pray_list["301"] = data_301
                self.all_data_list[each_dir]["data_301"]["data_time"] = data_time_301
            if os.path.exists(f"pray_history/{each_dir}/original_data/400.pickle"):
                data_400 = pickle.load(open(f"pray_history/{each_dir}/original_data/400.pickle", "rb"))
                data_time_400 = time.strftime("%Y-%m-%d %H:%M:%S",
                                              time.localtime((os.path.getmtime(f"pray_history/{each_dir}/original_data/400.pickle"))))
                self.all_data_list[each_dir]["data_400"]["data"] = data_400
                self.loaded_pray_list.append("角色祈愿-2")
                self.pray_list["400"] = data_400
                self.all_data_list[each_dir]["data_400"]["data_time"] = data_time_400
            if os.path.exists(f"pray_history/{each_dir}/original_data/302.pickle"):
                data_302 = pickle.load(open(f"pray_history/{each_dir}/original_data/302.pickle", "rb"))
                data_time_302 = time.strftime("%Y-%m-%d %H:%M:%S",
                                              time.localtime((os.path.getmtime(f"pray_history/{each_dir}/original_data/302.pickle"))))
                self.all_data_list[each_dir]["data_302"]["data"] = data_302
                self.loaded_pray_list.append("武器祈愿")
                self.pray_list["302"] = data_302
                self.all_data_list[each_dir]["data_302"]["data_time"] = data_time_302
        # Pre: 多UID支持预备
        if self.all_data_list:
            self.target_uid = list(self.all_data_list.keys())[0]
            self.uid_current_uid_label.setText(f"{self.target_uid}")

    def file_check(self):
        if not os.path.exists("assets"):
            QMessageBox.critical(self, "错误", "未找到必要模块，请检查目录(assets)是否存在")
            sys.exit()
        if not os.path.exists("modules"):
            QMessageBox.critical(self, "错误", "未找到必要模块，请检查目录(modules)是否存在")
            sys.exit()
        if not os.path.exists("modules/about"):
            QMessageBox.critical(self, "错误", "未找到必要模块，请检查目录(modules)是否存在")
            sys.exit()
        if not os.path.exists("cache"):
            os.mkdir("cache")
        if not os.path.exists("pray_history"):
            os.mkdir("pray_history")
        if not os.path.exists("config.json"):
            QMessageBox.critical(self, "错误", "未找到配置文件")
            sys.exit()

    def debug_code(self):
        pass

    # UI Part
    def initUI(self):
        # Font
        if os.path.exists("assets/font.ttf"):
            self.global_font = QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont("assets/font.ttf"))
        # UID - Image
        self.uid_user_image.setFixedSize(30, 30)
        # UID
        self.uid_current_uid_label.setFont(QFont(self.global_font, 13))
        self.uid_announce_btn.setFixedWidth(70)
        self.uid_settings_btn.setFixedWidth(90)
        self.uid_about_btn.setFixedWidth(90)

        self.uid_announce_btn.clicked.connect(lambda: self.announce_window.show())
        self.uid_settings_btn.clicked.connect(lambda: self.settings_window.show())
        self.uid_about_btn.clicked.connect(lambda: self.about_window.show())
        # UID - Splitter
        self.uid_splitter.setFrameShape(QFrame.Shape.HLine)
        # All - Left - Top Layout
        self.left_list_label.setFont(QFont(self.global_font, 14))
        self.left_open_export_dir_btn.setFixedWidth(90)
        self.left_refresh_btn.setFixedWidth(90)

        self.left_open_export_dir_btn.clicked.connect(self.left_open_export_dir)
        self.left_refresh_btn.clicked.connect(self.refreshData)
        # All - Left - Pray List
        self.left_pray_list.setFixedWidth(600)
        self.left_pray_list.setColumnCount(5)
        self.left_pray_list.setHorizontalHeaderLabels(["序号", "类型", "名称", "时间", "模式"])
        self.left_pray_list.setColumnWidth(0, 55)
        self.left_pray_list.setColumnWidth(1, 60)
        self.left_pray_list.setColumnWidth(2, 180)
        self.left_pray_list.setColumnWidth(3, 230)
        self.left_pray_list.setColumnWidth(4, 50)
        self.left_pray_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.left_pray_list.setShowGrid(False)
        self.left_pray_list.verticalHeader().setHidden(True)
        self.left_pray_list.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.left_pray_list.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.left_pray_list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # All - Left - Pray Mode Layout
        if not hide_new:
            self.left_pray_mode_100_btn.clicked.connect(self.left_pray_list_100_change)
        self.left_pray_mode_200_btn.clicked.connect(self.left_pray_list_200_change)
        self.left_pray_mode_301_btn.clicked.connect(self.left_pray_list_301_change)
        # self.left_pray_mode_400_btn.clicked.connect(self.left_pray_list_400_change)
        self.left_pray_mode_302_btn.clicked.connect(self.left_pray_list_302_change)
        # All - Splitter
        self.splitter.setFrameShape(QFrame.Shape.VLine)
        # All - Right - Top Layout
        self.right_label.setFont(QFont(self.global_font, 14))
        self.right_top_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        # All - Right - Analysis Layout
        self.right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.right_analysis_basic_label.setFont(QFont(self.global_font, 12))
        self.right_analysis_right_label.setFont(QFont(self.global_font, 12))
        self.right_analysis_basic_5_list_textEdit.setFixedHeight(90)
        self.right_analysis_basic_5_list_textEdit.setReadOnly(True)
        self.right_analysis_basic_4_list_textEdit.setFixedHeight(90)
        self.right_analysis_basic_4_list_textEdit.setReadOnly(True)
        self.right_analysis_right_weapon_alert_label.hide()
        self.right_analysis_right_weapon_alert_label.setStyleSheet("background-color: gray; border-radius: 10px; padding: 5px;")

    def allBtnStatusChange(self, is_enabled: bool):
        if not hide_new:
            self.left_pray_mode_100_btn.setEnabled(is_enabled)
        self.left_pray_mode_200_btn.setEnabled(is_enabled)
        self.left_pray_mode_301_btn.setEnabled(is_enabled)
        # self.left_pray_mode_400_btn.setEnabled(is_enabled)
        self.left_pray_mode_302_btn.setEnabled(is_enabled)
        self.left_refresh_btn.setEnabled(is_enabled)
        self.uid_settings_btn.setEnabled(is_enabled)

    # Left Function Part
    def left_open_export_dir(self):
        if self.target_uid:
            os.startfile(f"pray_history\\{self.target_uid}\\export\\")
        else:
            QMessageBox.critical(self, "错误", "未找到数据，请先更新数据")

    # Pray Mode Part
    def left_pray_list_100_change(self):
        self.right_analysis_right_weapon_alert_label.hide()
        if hide_new:
            return
        if "新手祈愿" in self.loaded_pray_list:
            self.refreshList("新手祈愿")
            self.left_status_label.setText("状态: 已读取新手祈愿")
            self.left_update_time_label.setText(f"数据时间: {self.all_data_list[self.target_uid]['data_100']['data_time']}")
        else:
            QMessageBox.warning(self, "警告", "未找到新手祈愿记录，请更新数据后重试\n也有可能没抽过")
            return

    def left_pray_list_200_change(self):
        self.right_analysis_right_weapon_alert_label.hide()
        if "常驻祈愿" in self.loaded_pray_list:
            self.refreshList("常驻祈愿")
            self.left_status_label.setText("状态: 已读取常驻祈愿")
            self.left_update_time_label.setText(f"数据时间: {self.all_data_list[self.target_uid]['data_200']['data_time']}")
        else:
            QMessageBox.warning(self, "警告", "未找到常驻祈愿记录，请更新数据后重试\n也有可能没抽过")
            return

    def left_pray_list_301_change(self):
        self.right_analysis_right_weapon_alert_label.hide()
        if "角色祈愿" in self.loaded_pray_list:
            self.refreshList("角色活动祈愿")
            self.left_status_label.setText("状态: 已读取角色祈愿")
            self.left_update_time_label.setText(f"数据时间: {self.all_data_list[self.target_uid]['data_301']['data_time']}")
        else:
            QMessageBox.warning(self, "警告", "未找到角色祈愿记录，请更新数据后重试\n也有可能没抽过")
            return

    def left_pray_list_400_change(self):
        self.right_analysis_right_weapon_alert_label.hide()
        if "角色祈愿-2" in self.loaded_pray_list:
            self.refreshList("角色活动祈愿-2")
            self.left_status_label.setText("状态: 已读取角色祈愿-2")
            self.left_update_time_label.setText(f"数据时间: {self.all_data_list[self.target_uid]['data_400']['data_time']}")
        else:
            QMessageBox.warning(self, "警告", "未找到角色祈愿-2记录，请更新数据后重试\n也有可能没抽过")
            return

    def left_pray_list_302_change(self):
        self.right_analysis_right_weapon_alert_label.show()
        if "武器祈愿" in self.loaded_pray_list:
            self.refreshList("武器祈愿")
            self.left_status_label.setText("状态: 已读取武器祈愿")
            self.left_update_time_label.setText(f"数据时间: {self.all_data_list[self.target_uid]['data_302']['data_time']}")
        else:
            QMessageBox.warning(self, "警告", "未找到武器祈愿记录，请更新数据后重试\n也有可能没抽过")
            return

    # Data Update Part
    def refreshData(self):
        global hide_new
        if not os.path.exists("interact"):
            open("interact", 'w')
        if os.path.exists("requestUrl.txt"):
            os.remove("requestUrl.txt")
        hide_new = json.loads(open("config.json", 'r').read())["settings"]["hide_new"]
        time.sleep(0.5)
        ex_module = subprocess.Popen("modules/GenshinProxyServer.exe")
        ex_module.wait()
        if not os.path.exists("requestUrl.txt"):
            QMessageBox.information(self, "提示", "代理服务器已被人为关闭")
            return
        global gachaUrl
        gachaUrl = open("requestUrl.txt", 'r').read()
        self.left_pray_list_thread_execute()

    # Pray List Thread
    def left_pray_list_thread_execute(self):
        self.allBtnStatusChange(False)
        self.get_pray_list_thread.start()
        self.get_pray_list_thread.trigger.connect(self.left_status_label_change)

    # Pray List Part
    def left_status_label_change(self, msg: str):  # 用于更改左侧列表下方的状态
        self.left_status_label.setText(f"状态: {msg}")
        if msg == "全部列表读取完毕":
            self.left_list_label.setText("祈愿列表")
            self.clearList()
            self.pre_generate()
            self.allBtnStatusChange(True)

    def clearList(self):  # 清空左侧列表
        [self.left_pray_list.removeRow(0) for _ in range(self.left_pray_list.rowCount())]

    def refreshList(self, pray_mode: str):  # 刷新左侧列表(清空左侧列表->重新生成)
        # 清空列表
        self.clearList()
        # 重新生成
        self.left_list_label.setText(f"祈愿列表 - {pray_mode}")
        self.right_label.setText(f"分析 - {pray_mode}")
        if gachaType[pray_mode] == "100" and not hide_new:
            data_list = self.pray_list["100"]
        else:
            data_list = self.pray_list[gachaType[pray_mode]]
        for i in data_list:
            self.addRow(len(data_list), i[0], i[1], i[2], "单抽")
        if len(data_list) >= 10:
            time_tmp = [i[2] for i in data_list]
            pos = 0
            while pos < len(data_list) - 9:
                if time_tmp[pos] == time_tmp[pos + 1]:
                    for i in range(pos, pos + 10):
                        self.left_pray_list.item(i, 4).setText(f"十连-{10 - i + pos}")
                    pos += 9
                pos += 1
        # 重新生成右侧分析
        analyser = analysis.Analysis(data_list, gachaType[pray_mode])
        try:
            percent_5 = round(analyser.get_5()[1]/len(data_list)*100, 2)
            percent_4 = round(analyser.get_4()[1]/len(data_list)*100, 2)
            percent_3 = round(analyser.get_3()/len(data_list)*100, 2)
        except ZeroDivisionError:
            percent_3, percent_4, percent_5 = "0.0", "0.0", "0.0"
        self.right_analysis_basic_total_label.setText(f"祈愿数: {len(data_list)}")
        self.right_analysis_basic_5_label.setText(f"5星数量: {analyser.get_5()[1]} ({percent_5}%)")
        self.right_analysis_basic_5_list_textEdit.setText(','.join(analyser.get_5()[0]))
        self.right_analysis_basic_4_label.setText(f"4星数量: {analyser.get_4()[1]} ({percent_4}%)")
        self.right_analysis_basic_4_list_textEdit.setText(','.join(analyser.get_4()[0]))
        self.right_analysis_basic_3_label.setText(f"3星数量: {analyser.get_3()} ({percent_3}%)")
        self.right_analysis_right_guarantee_label.setText(analyser.guarantee())

    def setColor(self, name: str, row: int):  # 设置某一列的颜色
        if name in analysis.weapon_4_list or name in analysis.character_4_list:
            selected_color = gachaItemLevelColor[4]
        elif name in analysis.weapon_5_list or name in analysis.character_5_list:
            selected_color = gachaItemLevelColor[5]
            for each_item in range(5):
                self.left_pray_list.item(row, each_item).setForeground(QBrush(QColor(0, 0, 0)))
        else:
            return
        for each_item in range(5):
            self.left_pray_list.item(row, each_item).setBackground(QBrush(selected_color))

    def addRow(self, data_length, typ, name, t, gacha_mode):  # 添加一行
        row = self.left_pray_list.rowCount()
        self.left_pray_list.setRowCount(row + 1)
        self.left_pray_list.setItem(row, 0, QTableWidgetItem())
        self.left_pray_list.item(row, 0).setText(str(data_length - row))
        self.left_pray_list.setItem(row, 1, QTableWidgetItem())
        self.left_pray_list.item(row, 1).setText(typ)
        self.left_pray_list.setItem(row, 2, QTableWidgetItem())
        self.left_pray_list.item(row, 2).setText(name)
        self.left_pray_list.setItem(row, 3, QTableWidgetItem())
        self.left_pray_list.item(row, 3).setText(t)
        self.left_pray_list.setItem(row, 4, QTableWidgetItem())
        self.left_pray_list.item(row, 4).setText(gacha_mode)
        self.setColor(name, row)
        self.left_pray_list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.left_pray_list.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)


class LeftPrayListThread(QThread):
    trigger = pyqtSignal(str)

    def __init__(self, parent=None):
        super(LeftPrayListThread, self).__init__(parent)
        self.uid = ""

    def run(self):
        export_data_list = []
        for key in gachaType.keys():
            if (hide_new and key == "新手祈愿") or key == "角色活动祈愿-2":
                continue
            global gachaTarget
            gachaTarget = gachaType[key]
            data, proceed_data = [], []
            page, old_page, old_end_id, end_id = 1, 1, 0, 0
            url = gachaUrl.split('&')
            url[-4] = f"gacha_type={gachaTarget}"
            target_url = '&'.join(url)
            rep = requests.get(target_url).json()
            try:
                self.uid = rep['data']["list"][0]['uid']
                export_data['info']['uid'] = self.uid
            except IndexError:
                pass
            while True:
                try:
                    target_url = target_url.replace(f"page={old_page}", f"page={page}").replace(f"end_id={old_end_id}",
                                                                                                f"end_id={end_id}")
                    rep_start_time = time.time()
                    rep = requests.get(target_url).json()
                    rep_end_time = time.time()
                    if rep["data"] is None:
                        break
                    tmp = rep["data"]["list"]
                    for i in tmp:
                        each_data = {"gacha_type": i["gacha_type"], "count": "1", "time": i["time"], "name": i['name'],
                                     "item_type": i["item_type"],
                                     "rank_type": i["rank_type"], "id": i["id"],
                                     "uigf_gacha_type": uigfGachaType[i["gacha_type"]]}
                        proceed_data.append([i['item_type'], i['name'], i['time']])
                        export_data_list.append(each_data)
                    self.usleep(400)  # 防止API检测到频繁请求而拒止
                    old_page, old_end_id = page, end_id
                    page += 1
                    if type(page) == int:
                        self.trigger.emit(f"正在读取第{str(page - 1)}页记录 - {key} - 耗时{round(rep_end_time - rep_start_time, 2)}s")
                    end_id = rep["data"]["list"][-1]["id"]
                except IndexError or TypeError:
                    break
            self.trigger.emit(f"{key}读取完毕")
            for each_path in [f"pray_history/{self.uid}", f"pray_history/{self.uid}/original_data", f"pray_history/{self.uid}/export"]:
                os.mkdir(each_path) if not os.path.exists(each_path) else None
            with open(f'pray_history/{self.uid}/original_data/{gachaTarget}.pickle', 'wb') as f:
                pickle.dump(proceed_data, f)
        export_data["info"]["export_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        export_data["list"] = export_data_list
        open(f"pray_history/{self.uid}/export/{self.uid}_export_data.json", "w", encoding="utf-8").write(
            json.dumps(export_data, indent=2, sort_keys=True, ensure_ascii=False))
        self.trigger.emit("全部列表读取完毕")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(os.path.join(basedir, 'assets/icon.ico')))
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    start = MainForm()
    start.show()
    sys.exit(app.exec())
