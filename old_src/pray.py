# -*- coding:utf-8 -*-
import json
import os
import sys
import time
from pickle import load, dump
from subprocess import Popen
from sys import exit, argv
from requests import get
from PySide6 import QtCore, QtGui
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont, QBrush, QColor, QFontDatabase
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QWidget, QMainWindow, QHBoxLayout, QTableWidget, QPushButton, QApplication, QVBoxLayout, \
    QMessageBox, QAbstractItemView, QHeaderView, QLabel, QFrame, QTextEdit, QTableWidgetItem, QComboBox, QFileDialog

from modules.api import information, analysis, transformation
from modules.sub_widgets import about_widget, announce_widget, settings_widget
from modules.file_verification import verification

gachaUrl = ""
GACHATYPE = {"新手祈愿": "100", "常驻祈愿": "200", "角色活动祈愿": "301", "角色活动祈愿-2": "400", "武器祈愿": "302"}
REV_GACHATYPE = {v: k for k, v in GACHATYPE.items()}
UIGF_GACHATYPE = {"100": "100", "200": "200", "301": "301", "400": "301", "302": "302"}
UIGF_VERSION = "v2.2"
WORKING_DIR = '/'.join(sys.argv[0].split('/')[:-1]) + '/'
gachaTarget = ""
gachaItemLevelColor = {4: QColor(132, 112, 255), 5: QColor(255, 185, 15)}
export_data = {"info": {"uid": "", "lang": "zh-cn", "export_time": ""}, "list": []}

CONFIG_PATH = "config.json"

basedir = os.path.dirname(__file__)
version = "Unknown"
hide_new = json.loads(open(CONFIG_PATH, "r", encoding="utf-8").read())["settings"]["hide_new"]

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
        self.setFixedSize(1250, 690)
        self.global_font = "Microsoft YaHei"

        # Pray List Init
        self.loaded_pray_list = []
        self.current_show_list = None
        self.pray_list = {"100": None, "200": None, "301": None, "400": None, "302": None}

        # Multi-process
        self.get_pray_list_thread = LeftPrayListThread()

        # API
        self.api_information = information.Information()
        self.able_to_get_announce = True and len(self.api_information.announce_data)
        global version
        version = information.get_exporter_version(CONFIG_PATH)

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
        self.uid_current_uid_combobox = QComboBox(self)
        self.uid_json_import_btn = QPushButton("导入")
        self.uid_json_export_btn = QPushButton("导出")

        self.uid_label_splitter = QFrame(self)

        self.uid_announce_btn = QPushButton("游戏公告")
        self.uid_up_character_label = QLabel("当期UP角色: 未知")
        self.uid_up_weapon_label = QLabel("当期UP武器: 未知")
        self.uid_settings_btn = QPushButton("设置")
        self.uid_about_btn = QPushButton("关于")
        self.uid_h_layout.addWidget(self.uid_user_image)
        self.uid_h_layout.addWidget(self.uid_current_uid_combobox)
        self.uid_h_layout.addWidget(self.uid_json_import_btn)
        self.uid_h_layout.addWidget(self.uid_json_export_btn)
        self.uid_h_layout.addWidget(self.uid_label_splitter)
        self.uid_h_layout.addWidget(self.uid_announce_btn)
        self.uid_h_layout.addWidget(self.uid_up_character_label)
        self.uid_h_layout.addWidget(self.uid_up_weapon_label)
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
        self.left_pray_mode_302_btn = QPushButton("武器祈愿")
        self.left_pray_mode_h_layout.addWidget(self.left_pray_mode_200_btn)
        self.left_pray_mode_h_layout.addWidget(self.left_pray_mode_301_btn)
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
        self.analyser = None

        # File Verification
        self.file_verification = verification.Verification()
        self.file_check()

        self.pre_generate()
        self.initUI()

        # Child Windows
        self.announce_window = announce_widget.Announce()
        self.about_window = about_widget.About()
        self.settings_window = settings_widget.Settings()

        self.debug_code()

    def pre_generate(self):
        for each_dir in os.listdir("pray_history"):
            self.all_data_list.update({each_dir: {"data_100": {"data": [], "data_time": ""},
                                                  "data_200": {"data": [], "data_time": ""},
                                                  "data_301": {"data": [], "data_time": ""},
                                                  "data_400": {"data": [], "data_time": ""},
                                                  "data_302": {"data": [], "data_time": ""}}})
            if os.path.exists(f"pray_history/{each_dir}/original_data/100.pickle") and not hide_new:
                data_100 = load(open(f"pray_history/{each_dir}/original_data/100.pickle", "rb"))
                data_time_100 = time.strftime("%Y-%m-%d %H:%M:%S",
                                              time.localtime((os.path.getmtime(
                                                  f"pray_history/{each_dir}/original_data/100.pickle"))))
                self.all_data_list[each_dir]["data_100"]["data"] = data_100
                self.loaded_pray_list.append("新手祈愿")
                self.pray_list["100"] = data_100
                self.all_data_list[each_dir]["data_100"]["data_time"] = data_time_100
            if os.path.exists(f"pray_history/{each_dir}/original_data/200.pickle"):
                data_200 = load(open(f"pray_history/{each_dir}/original_data/200.pickle", "rb"))
                data_time_200 = time.strftime("%Y-%m-%d %H:%M:%S",
                                              time.localtime((os.path.getmtime(
                                                  f"pray_history/{each_dir}/original_data/200.pickle"))))
                self.all_data_list[each_dir]["data_200"]["data"] = data_200
                self.loaded_pray_list.append("常驻祈愿")
                self.pray_list["200"] = data_200
                self.all_data_list[each_dir]["data_200"]["data_time"] = data_time_200
            if os.path.exists(f"pray_history/{each_dir}/original_data/301.pickle"):
                data_301 = load(open(f"pray_history/{each_dir}/original_data/301.pickle", "rb"))
                data_time_301 = time.strftime("%Y-%m-%d %H:%M:%S",
                                              time.localtime((os.path.getmtime(
                                                  f"pray_history/{each_dir}/original_data/301.pickle"))))
                self.all_data_list[each_dir]["data_301"]["data"] = data_301
                self.loaded_pray_list.append("角色活动祈愿")
                self.pray_list["301"] = data_301
                self.all_data_list[each_dir]["data_301"]["data_time"] = data_time_301
            if os.path.exists(f"pray_history/{each_dir}/original_data/400.pickle"):
                data_400 = load(open(f"pray_history/{each_dir}/original_data/400.pickle", "rb"))
                data_time_400 = time.strftime("%Y-%m-%d %H:%M:%S",
                                              time.localtime((os.path.getmtime(
                                                  f"pray_history/{each_dir}/original_data/400.pickle"))))
                self.all_data_list[each_dir]["data_400"]["data"] = data_400
                self.loaded_pray_list.append("角色活动祈愿-2")
                self.pray_list["400"] = data_400
                self.all_data_list[each_dir]["data_400"]["data_time"] = data_time_400
            if os.path.exists(f"pray_history/{each_dir}/original_data/302.pickle"):
                data_302 = load(open(f"pray_history/{each_dir}/original_data/302.pickle", "rb"))
                data_time_302 = time.strftime("%Y-%m-%d %H:%M:%S",
                                              time.localtime((os.path.getmtime(
                                                  f"pray_history/{each_dir}/original_data/302.pickle"))))
                self.all_data_list[each_dir]["data_302"]["data"] = data_302
                self.loaded_pray_list.append("武器祈愿")
                self.pray_list["302"] = data_302
                self.all_data_list[each_dir]["data_302"]["data_time"] = data_time_302
        self.uid_current_uid_combobox.clear()
        self.uid_current_uid_combobox.addItems(self.all_data_list.keys())
        if self.all_data_list:
            ori_config_json = json.loads(open("config.json", 'r').read())
            latest_uid = ori_config_json["settings"]["latest_uid_selected"]
            if not latest_uid:
                self.target_uid = list(self.all_data_list.keys())[0]
                self.uid_current_uid_combobox.setCurrentIndex(0)
            elif latest_uid in self.all_data_list.keys():
                self.target_uid = latest_uid
                self.uid_current_uid_combobox.setCurrentIndex(self.uid_current_uid_combobox.findText(latest_uid))
            elif latest_uid not in self.all_data_list.keys():
                self.target_uid = list(self.all_data_list.keys())[0]
                self.uid_current_uid_combobox.setCurrentIndex(0)
            ori_config_json["settings"]["latest_uid_selected"] = self.target_uid
            open(f"config.json", "w", encoding="utf-8").write(
                json.dumps(ori_config_json, indent=2, sort_keys=True, ensure_ascii=False))
            self.uid_current_uid_combobox.setCurrentText(self.target_uid)
        if len(self.loaded_pray_list) >= 3:
            self.analyser = analysis.Analysis(self.target_uid, self.all_data_list)
        self.uid_changed_regenerate()

    def uid_json_import(self):
        import_json_path = QFileDialog.getOpenFileName(self, "选择UIGF-Json文件", "./", "Json文件(*.json)")[0]
        if not import_json_path:
            return
        json_detail = json.loads(open(import_json_path, "r", encoding="utf-8").read())
        try:
            json_info = json_detail["info"]
            if json_info['uid'] in self.all_data_list.keys():
                QMessageBox.information(self, "提示",
                                        f"该UID已存在\n若仍要导入，请删除原有UID的数据(pray_history/{json_info['uid']})后再导入")
                return
            json_info_show = f"确认导入?\n\nUID: {json_info['uid']}\n导出时间: {json_info['export_time']}\n导出软件: {json_info['export_app']} - {json_info['export_app_version']}"
        except KeyError:
            QMessageBox.critical(self, "错误", "导入的Json文件格式错误")
            return
        reply = QMessageBox.question(self, "导入", json_info_show,
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.all_data_list[json_info["uid"]] = json_detail
            self.uid_current_uid_combobox.addItem(json_info["uid"])
            self.uid_current_uid_combobox.setCurrentIndex(self.uid_current_uid_combobox.findText(json_info["uid"]))
            self.target_uid = json_info["uid"]
            self.uid_current_uid_combobox.currentIndexChanged.emit(self.uid_current_uid_combobox.currentIndex())
            os.mkdir(f"pray_history/{json_info['uid']}")
            os.mkdir(f"pray_history/{json_info['uid']}/original_data")
            os.mkdir(f"pray_history/{json_info['uid']}/export")
            import_data = transformation.jsonToOriginal(json_detail)
            for each_data in import_data:
                if import_data[each_data]:
                    self.loaded_pray_list.append(REV_GACHATYPE[each_data])
                    dump(import_data[each_data],
                         open(f"pray_history/{json_info['uid']}/original_data/{each_data}.pickle", "wb"))
            self.pre_generate()
            QMessageBox.information(self, "提示", "导入成功")
        return

    def uid_json_export(self):
        json_export_data = export_data
        json_export_data["info"]["export_app"] = "sangonomiya"
        json_export_data["info"]["uigf_version"] = UIGF_VERSION
        json_export_data["info"]["export_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        json_export_data["info"]["export_timestamp"] = int(round(time.time() * 1000))
        json_export_data['info']['uid'] = self.target_uid
        json_export_data["info"]["export_app_version"] = version
        json_export_data["list"] = transformation.OriginalToJson(f"pray_history/{self.target_uid}/original_data/",
                                                                 os.listdir(
                                                                     f"pray_history/{self.target_uid}/original_data/"))
        export_json_path = \
            QFileDialog.getSaveFileName(self, "保存UIGF-Json文件", f"./{self.target_uid}_export_data.json",
                                        "Json文件(*.json)")[0]
        if not export_json_path:
            return
        open(export_json_path, "w", encoding="utf-8").write(
            json.dumps(json_export_data, indent=2, sort_keys=True, ensure_ascii=False))

    def uid_changed_regenerate(self):
        self.target_uid = self.uid_current_uid_combobox.currentText()
        if not self.target_uid:
            return
        ori_config_json = json.loads(open("config.json", 'r').read())
        ori_config_json["settings"]["latest_uid_selected"] = self.target_uid
        open(f"config.json", "w", encoding="utf-8").write(
            json.dumps(ori_config_json, indent=4, sort_keys=True, ensure_ascii=False))
        for each in self.pray_list.keys():
            try:
                self.pray_list[each] = self.all_data_list[self.target_uid][f"data_{each}"]["data"]
            except KeyError:
                continue
        self.analyser = analysis.Analysis(self.target_uid, self.all_data_list)
        if self.current_show_list:
            self.refreshList(self.current_show_list)
            self.analysis_regenerate(GACHATYPE[self.current_show_list],
                                     self.pray_list[GACHATYPE[self.current_show_list]])

    def file_check(self):
        result = self.file_verification.exist()
        if not result[1]:
            QMessageBox.critical(self, "文件检查", f"发现文件不完整:\n{result[0]}", QMessageBox.StandardButton.Ok)
            exit()

    def debug_code(self):
        pass

    # UI Part
    def initUI(self):
        # Font
        if os.path.exists("assets/font.ttf"):
            self.global_font = QFontDatabase.applicationFontFamilies(
                QFontDatabase.addApplicationFont("assets/font.ttf"))
        # UID - Image
        self.uid_user_image.setFixedSize(30, 30)
        # UID
        self.uid_current_uid_combobox.setFont(QFont(self.global_font, 13))
        self.uid_current_uid_combobox.setFixedWidth(125)
        self.uid_json_import_btn.setFixedWidth(35)
        self.uid_json_export_btn.setFixedWidth(35)
        self.uid_label_splitter.setFrameShape(QFrame.Shape.VLine)
        self.uid_announce_btn.setFixedWidth(70)
        self.uid_up_character_label.setText(f"当期UP角色: {''.join(self.api_information.get_up_character())}")
        self.uid_up_weapon_label.setText(f"当期UP武器: {''.join(self.api_information.get_up_weapon())}")
        self.uid_settings_btn.setFixedWidth(90)
        self.uid_about_btn.setFixedWidth(90)

        self.uid_current_uid_combobox.currentIndexChanged.connect(self.uid_changed_regenerate)
        self.uid_json_import_btn.clicked.connect(self.uid_json_import)
        self.uid_json_export_btn.clicked.connect(self.uid_json_export)
        if not self.able_to_get_announce:
            self.uid_announce_btn.setEnabled(False)
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
            self.left_pray_mode_100_btn.clicked.connect(lambda: self.left_pray_list_btn_change("新手祈愿"))
        self.left_pray_mode_200_btn.clicked.connect(lambda: self.left_pray_list_btn_change("常驻祈愿"))
        self.left_pray_mode_301_btn.clicked.connect(lambda: self.left_pray_list_btn_change("角色活动祈愿"))
        self.left_pray_mode_302_btn.clicked.connect(lambda: self.left_pray_list_btn_change("武器祈愿"))
        # All - Splitter
        self.splitter.setFrameShape(QFrame.Shape.VLine)
        # All - Right - Top Layout
        self.right_label.setFont(QFont(self.global_font, 14))
        self.right_top_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        # All - Right - Analysis Layout
        self.right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.right_analysis_basic_label.setFont(QFont(self.global_font, 12))
        self.right_analysis_right_label.setFont(QFont(self.global_font, 12))
        self.right_analysis_basic_5_list_textEdit.setFixedHeight(135)
        self.right_analysis_basic_5_list_textEdit.setFixedWidth(600)
        self.right_analysis_basic_5_list_textEdit.setReadOnly(True)
        self.right_analysis_basic_4_list_textEdit.setFixedHeight(135)
        self.right_analysis_basic_4_list_textEdit.setFixedWidth(600)
        self.right_analysis_basic_4_list_textEdit.setReadOnly(True)
        self.right_analysis_right_weapon_alert_label.hide()
        self.right_analysis_right_weapon_alert_label.setStyleSheet(
            "background-color: gray; border-radius: 10px; padding: 5px;")

    def allBtnStatusChange(self, is_enabled: bool):
        self.uid_current_uid_combobox.setEnabled(is_enabled)
        self.uid_json_import_btn.setEnabled(is_enabled)
        self.uid_json_export_btn.setEnabled(is_enabled)
        if not hide_new:
            self.left_pray_mode_100_btn.setEnabled(is_enabled)
        self.left_pray_mode_200_btn.setEnabled(is_enabled)
        self.left_pray_mode_301_btn.setEnabled(is_enabled)
        self.left_pray_mode_302_btn.setEnabled(is_enabled)
        self.left_refresh_btn.setEnabled(is_enabled)
        self.uid_settings_btn.setEnabled(is_enabled)

    def analysis_regenerate(self, pray_mode, data_list):
        try:
            percent_5 = round(self.analyser.get_5(pray_mode)[1] / len(data_list) * 100, 2)
            percent_4 = round(self.analyser.get_4(pray_mode)[1] / len(data_list) * 100, 2)
            percent_3 = round(self.analyser.get_3(pray_mode) / len(data_list) * 100, 2)
        except ZeroDivisionError:
            percent_3, percent_4, percent_5 = "0.0", "0.0", "0.0"
        self.right_analysis_basic_total_label.setText(f"祈愿数: {len(data_list)}")
        self.right_analysis_basic_5_label.setText(f"5星数量: {self.analyser.get_5(pray_mode)[1]} ({percent_5}%)")
        self.right_analysis_basic_5_list_textEdit.setText(','.join(self.analyser.get_5(pray_mode)[0]))
        self.right_analysis_basic_4_label.setText(f"4星数量: {self.analyser.get_4(pray_mode)[1]} ({percent_4}%)")
        self.right_analysis_basic_4_list_textEdit.setText(','.join(self.analyser.get_4(pray_mode)[0]))
        self.right_analysis_basic_3_label.setText(f"3星数量: {self.analyser.get_3(pray_mode)} ({percent_3}%)")
        self.right_analysis_right_guarantee_label.setText(self.analyser.guarantee(pray_mode))

    # Left Function Part
    def left_open_export_dir(self):
        if self.target_uid:
            os.startfile(f"pray_history\\{self.target_uid}\\export\\")
        else:
            QMessageBox.critical(self, "错误", "未找到数据，请先更新数据")

    # Pray Mode Part
    def left_pray_list_btn_change(self, btn_type):
        if btn_type == "武器祈愿":
            self.right_analysis_right_weapon_alert_label.show()
        else:
            self.right_analysis_right_weapon_alert_label.hide()
        if btn_type == "新手祈愿" and hide_new:
            return
        if btn_type in self.loaded_pray_list and self.all_data_list[self.target_uid][f'data_{GACHATYPE[btn_type]}']['data_time']:
            self.refreshList(btn_type)
            self.current_show_list = btn_type
            self.left_status_label.setText(f"状态: 已读取{btn_type}")
            self.left_update_time_label.setText(
                f"数据时间: {self.all_data_list[self.target_uid][f'data_{GACHATYPE[btn_type]}']['data_time']}")
        else:
            QMessageBox.warning(self, "警告", f"未找到{btn_type}记录，请更新数据后重试\n也有可能没抽过")
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
        ex_module = Popen("modules/GenshinProxyServer.exe")
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
            self.uid_current_uid_combobox.setCurrentText(self.target_uid)

    def clearList(self):  # 清空左侧列表
        [self.left_pray_list.removeRow(0) for _ in range(self.left_pray_list.rowCount())]

    def refreshList(self, pray_mode: str):  # 刷新左侧列表(清空左侧列表->重新生成)
        # 清空列表
        self.clearList()
        # 重新生成
        self.left_list_label.setText(f"祈愿列表 - {pray_mode}")
        self.right_label.setText(f"分析 - {pray_mode}")
        if GACHATYPE[pray_mode] == "100" and not hide_new:
            data_list = self.pray_list["100"]
        else:
            data_list = self.pray_list[GACHATYPE[pray_mode]]
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
        pray_mode = GACHATYPE[pray_mode]
        self.analysis_regenerate(pray_mode, data_list)

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
    trigger = Signal(str)

    def __init__(self, parent=None):
        super(LeftPrayListThread, self).__init__(parent)
        self.uid = ""

    def run(self):
        export_data_list = []
        json_export_data = export_data
        for key in GACHATYPE.keys():
            if hide_new and key == "新手祈愿":
                continue
            global gachaTarget
            gachaTarget = GACHATYPE[key]
            data, proceed_data = [], []
            page, old_page, old_end_id, end_id = 1, 1, 0, 0
            url = gachaUrl.split('&')
            url[-4] = f"gacha_type={gachaTarget}"
            target_url = '&'.join(url)
            rep = get(target_url).json()
            try:
                self.uid = rep['data']["list"][0]['uid']
                json_export_data['info']['uid'] = self.uid
            except IndexError:
                pass
            while True:
                try:
                    target_url = target_url.replace(f"page={old_page}", f"page={page}").replace(f"end_id={old_end_id}",
                                                                                                f"end_id={end_id}")
                    rep_start_time = time.time()
                    rep = get(target_url).json()
                    rep_end_time = time.time()
                    if rep["data"] is None:
                        break
                    tmp = rep["data"]["list"]
                    for i in tmp:
                        each_data = {"gacha_type": i["gacha_type"], "count": "1", "time": i["time"], "name": i['name'],
                                     "item_type": i["item_type"],
                                     "rank_type": i["rank_type"], "id": i["id"],
                                     "uigf_gacha_type": UIGF_GACHATYPE[i["gacha_type"]]}
                        proceed_data.append([i['item_type'], i['name'], i['time'], i['id'], i['rank_type']])
                        export_data_list.append(each_data)
                    self.usleep(400)  # 防止API检测到频繁请求而拒止
                    old_page, old_end_id = page, end_id
                    page += 1
                    if type(page) == int:
                        self.trigger.emit(
                            f"正在读取第{str(page - 1)}页记录 - {key} - 耗时{round(rep_end_time - rep_start_time, 2)}s")
                    end_id = rep["data"]["list"][-1]["id"]
                except IndexError or TypeError:
                    break
            self.trigger.emit(f"{key}读取完毕")
            for each_path in [f"pray_history/{self.uid}", f"pray_history/{self.uid}/original_data",
                              f"pray_history/{self.uid}/export"]:
                os.mkdir(each_path) if not os.path.exists(each_path) else None
            with open(f'pray_history/{self.uid}/original_data/{gachaTarget}.pickle', 'wb') as f:
                dump(proceed_data, f)
        json_export_data["info"]["export_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        json_export_data["info"]["export_timestamp"] = int(round(time.time() * 1000))
        json_export_data["info"]["export_app"] = "sangonomiya"
        json_export_data["info"]["export_app_version"] = version
        json_export_data["info"]["uigf_version"] = UIGF_VERSION
        json_export_data["list"] = export_data_list
        open(f"pray_history/{self.uid}/export/{self.uid}_export_data.json", "w", encoding="utf-8").write(
            json.dumps(json_export_data, indent=2, sort_keys=True, ensure_ascii=False))
        self.trigger.emit("全部列表读取完毕")


if __name__ == '__main__':
    app = QApplication(argv)
    app.setWindowIcon(QtGui.QIcon(os.path.join(basedir, 'assets/icon.ico')))
    start = MainForm()
    start.show()
    exit(app.exec())
