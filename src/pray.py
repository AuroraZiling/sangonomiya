# -*- coding:utf-8 -*-
import json
import os
import pickle
import subprocess
import sys
import time
import qdarkstyle
import requests
from PyQt6 import QtCore, QtWidgets, QtGui, QtSvg
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QBrush, QColor
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtWidgets import QWidget, QMainWindow, QHBoxLayout, QTableWidget, QPushButton, QApplication, QVBoxLayout, \
    QMessageBox, QAbstractItemView, QHeaderView, QLabel, QGridLayout, QFrame

from modules import result_list

gachaUrl = ""
gachaType = {"新手祈愿": "100", "常驻祈愿": "200", "角色活动祈愿": "301", "角色活动祈愿-2": "400", "武器祈愿": "302"}
uigfGachaType = {"100": "100", "200": "200", "301": "301", "400": "301", "302": "302"}
gachaTarget = ""
gachaItemLevelColor = {4: QColor(132, 112, 255), 5: QColor(255, 185, 15)}
export_data = {"info": {"uid": "", "lang": "zh-cn", "export_time": ""}, "list": []}

basedir = os.path.dirname(__file__)

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
        self.setFixedSize(1200, 600)

        # Pray List Init
        self.loaded_pray_list = []
        self.pray_100, self.pray_200, self.pray_301, self.pray_400, self.pray_302 = None, None, None, None, None

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
        self.uid_h_layout.addWidget(self.uid_user_image)
        self.uid_h_layout.addWidget(self.uid_current_uid_label)
        self.uid_splitter = QFrame(self)
        self.base_layout.addLayout(self.uid_h_layout)
        self.base_layout.addWidget(self.uid_splitter)

        # UI Left
        self.left_top_layout = QHBoxLayout(self)
        self.left_list_label = QLabel("祈愿记录")
        self.left_open_export_dir_btn = QPushButton("打开导出目录")
        self.left_refresh_btn = QPushButton("更新数据")
        self.left_settings_btn = QPushButton("设置")
        self.left_top_layout.addWidget(self.left_list_label)
        self.left_top_layout.addWidget(self.left_open_export_dir_btn)
        self.left_top_layout.addWidget(self.left_refresh_btn)
        self.left_top_layout.addWidget(self.left_settings_btn)
        self.left_layout.addLayout(self.left_top_layout)

        self.left_pray_list = QTableWidget(self)
        self.left_layout.addWidget(self.left_pray_list)

        self.left_pray_mode_h_layout = QHBoxLayout(self)
        self.left_pray_mode_100_btn = QPushButton("新手祈愿")
        self.left_pray_mode_200_btn = QPushButton("常驻祈愿")
        self.left_pray_mode_301_btn = QPushButton("角色祈愿")
        self.left_pray_mode_400_btn = QPushButton("角色祈愿-2")
        self.left_pray_mode_302_btn = QPushButton("武器祈愿")
        self.left_pray_mode_h_layout.addWidget(self.left_pray_mode_100_btn)
        self.left_pray_mode_h_layout.addWidget(self.left_pray_mode_200_btn)
        self.left_pray_mode_h_layout.addWidget(self.left_pray_mode_301_btn)
        self.left_pray_mode_h_layout.addWidget(self.left_pray_mode_400_btn)
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

        self.right_analysis_layout = QGridLayout(self)
        self.right_analysis_label = QLabel("暂不可用")
        self.right_analysis_layout.addWidget(self.right_analysis_label, 0, 0)

        self.right_layout.addLayout(self.right_top_layout)
        self.right_layout.addLayout(self.right_analysis_layout)

        self.all_layout.addLayout(self.left_layout)
        self.all_layout.addWidget(self.splitter)
        self.all_layout.addLayout(self.right_layout)
        self.base_layout.addLayout(self.all_layout)
        self.widget.setLayout(self.base_layout)
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
            if os.path.exists(f"pray_history/{each_dir}/original_data/100.pickle"):
                data_100 = pickle.load(open(f"pray_history/{each_dir}/original_data/100.pickle", "rb"))
                data_time_100 = time.strftime("%Y-%m-%d %H:%M:%S",
                                              time.localtime((os.path.getmtime(f"pray_history/{each_dir}/original_data/100.pickle"))))
                self.all_data_list[each_dir]["data_100"]["data"] = data_100
                self.loaded_pray_list.append("新手祈愿")
                self.pray_100 = data_100
                self.all_data_list[each_dir]["data_100"]["data_time"] = data_time_100
            if os.path.exists(f"pray_history/{each_dir}/original_data/200.pickle"):
                data_200 = pickle.load(open(f"pray_history/{each_dir}/original_data/200.pickle", "rb"))
                data_time_200 = time.strftime("%Y-%m-%d %H:%M:%S",
                                              time.localtime((os.path.getmtime(f"pray_history/{each_dir}/original_data/200.pickle"))))
                self.all_data_list[each_dir]["data_200"]["data"] = data_200
                self.loaded_pray_list.append("常驻祈愿")
                self.pray_200 = data_200
                self.all_data_list[each_dir]["data_200"]["data_time"] = data_time_200
            if os.path.exists(f"pray_history/{each_dir}/original_data/301.pickle"):
                data_301 = pickle.load(open(f"pray_history/{each_dir}/original_data/301.pickle", "rb"))
                data_time_301 = time.strftime("%Y-%m-%d %H:%M:%S",
                                              time.localtime((os.path.getmtime(f"pray_history/{each_dir}/original_data/301.pickle"))))
                self.all_data_list[each_dir]["data_301"]["data"] = data_301
                self.loaded_pray_list.append("角色祈愿")
                self.pray_301 = data_301
                self.all_data_list[each_dir]["data_301"]["data_time"] = data_time_301
            if os.path.exists(f"pray_history/{each_dir}/original_data/400.pickle"):
                data_400 = pickle.load(open(f"pray_history/{each_dir}/original_data/400.pickle", "rb"))
                data_time_400 = time.strftime("%Y-%m-%d %H:%M:%S",
                                              time.localtime((os.path.getmtime(f"pray_history/{each_dir}/original_data/400.pickle"))))
                self.all_data_list[each_dir]["data_400"]["data"] = data_400
                self.loaded_pray_list.append("角色祈愿-2")
                self.pray_400 = data_400
                self.all_data_list[each_dir]["data_400"]["data_time"] = data_time_400
            if os.path.exists(f"pray_history/{each_dir}/original_data/302.pickle"):
                data_302 = pickle.load(open(f"pray_history/{each_dir}/original_data/302.pickle", "rb"))
                data_time_302 = time.strftime("%Y-%m-%d %H:%M:%S",
                                              time.localtime((os.path.getmtime(f"pray_history/{each_dir}/original_data/302.pickle"))))
                self.all_data_list[each_dir]["data_302"]["data"] = data_302
                self.loaded_pray_list.append("武器祈愿")
                self.pray_302 = data_302
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
        if not os.path.exists("pray_history"):
            os.mkdir("pray_history")
        if not os.path.exists("export"):
            os.mkdir("export")

    def debug_code(self):
        pass

    # UI Part
    def initUI(self):
        # UID - Image
        self.uid_user_image.setFixedSize(30, 30)
        # UID - Label
        self.uid_current_uid_label.setFont(QFont("Microsoft YaHei", 13))
        # UID - Splitter
        self.uid_splitter.setFrameShape(QFrame.Shape.HLine)
        # All - Left - Top Layout
        self.left_list_label.setFont(QFont("Microsoft YaHei", 11))
        self.left_open_export_dir_btn.setFixedWidth(90)
        self.left_refresh_btn.setFixedWidth(90)
        self.left_settings_btn.setFixedWidth(90)
        self.left_settings_btn.setEnabled(False)  # Locked

        self.left_open_export_dir_btn.clicked.connect(lambda x: os.startfile("export"))
        self.left_refresh_btn.clicked.connect(self.refreshData)
        # All - Left - Pray List
        self.left_pray_list.setFixedWidth(560)
        self.left_pray_list.setColumnCount(4)
        self.left_pray_list.setHorizontalHeaderLabels(["序号", "类型", "名称", "时间"])
        self.left_pray_list.setColumnWidth(0, 60)
        self.left_pray_list.setColumnWidth(1, 60)
        self.left_pray_list.setColumnWidth(2, 180)
        self.left_pray_list.setColumnWidth(3, 230)
        self.left_pray_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.left_pray_list.setShowGrid(False)
        self.left_pray_list.verticalHeader().setHidden(True)
        self.left_pray_list.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.left_pray_list.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.left_pray_list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # All - Left - Pray Mode Layout
        self.left_pray_mode_100_btn.clicked.connect(self.left_pray_list_100_change)
        self.left_pray_mode_200_btn.clicked.connect(self.left_pray_list_200_change)
        self.left_pray_mode_301_btn.clicked.connect(self.left_pray_list_301_change)
        self.left_pray_mode_400_btn.clicked.connect(self.left_pray_list_400_change)
        self.left_pray_mode_302_btn.clicked.connect(self.left_pray_list_302_change)
        # All - Splitter
        self.splitter.setFrameShape(QFrame.Shape.VLine)
        # All - Right - Top Layout
        self.right_label.setFont(QFont("Microsoft YaHei", 11))
        self.right_top_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        # All - Right - Analysis Layout
        self.right_analysis_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def allBtnStatusChange(self, is_enabled: bool):
        self.left_pray_mode_100_btn.setEnabled(is_enabled)
        self.left_pray_mode_200_btn.setEnabled(is_enabled)
        self.left_pray_mode_301_btn.setEnabled(is_enabled)
        self.left_pray_mode_400_btn.setEnabled(is_enabled)
        self.left_pray_mode_302_btn.setEnabled(is_enabled)
        self.left_refresh_btn.setEnabled(is_enabled)
        # Locked
        # self.left_settings_btn.setEnabled(is_enabled)

    # Pray Mode Part
    def left_pray_list_100_change(self):
        if "新手祈愿" in self.loaded_pray_list:
            self.refreshList("新手祈愿")
            self.left_status_label.setText("状态: 已读取新手祈愿")
            self.left_update_time_label.setText(f"数据时间: {self.all_data_list[self.target_uid]['data_100']['data_time']}")
        else:
            QMessageBox.warning(self, "警告", "未找到新手祈愿记录，请更新数据后重试\n也有可能没抽过")
            return

    def left_pray_list_200_change(self):
        if "常驻祈愿" in self.loaded_pray_list:
            self.refreshList("常驻祈愿")
            self.left_status_label.setText("状态: 已读取常驻祈愿")
            self.left_update_time_label.setText(f"数据时间: {self.all_data_list[self.target_uid]['data_200']['data_time']}")
        else:
            QMessageBox.warning(self, "警告", "未找到常驻祈愿记录，请更新数据后重试\n也有可能没抽过")
            return

    def left_pray_list_301_change(self):
        if "角色祈愿" in self.loaded_pray_list:
            self.refreshList("角色活动祈愿")
            self.left_status_label.setText("状态: 已读取角色祈愿")
            self.left_update_time_label.setText(f"数据时间: {self.all_data_list[self.target_uid]['data_301']['data_time']}")
        else:
            QMessageBox.warning(self, "警告", "未找到角色祈愿记录，请更新数据后重试\n也有可能没抽过")
            return

    def left_pray_list_400_change(self):
        if "角色祈愿-2" in self.loaded_pray_list:
            self.refreshList("角色活动祈愿-2")
            self.left_status_label.setText("状态: 已读取角色祈愿-2")
            self.left_update_time_label.setText(f"数据时间: {self.all_data_list[self.target_uid]['data_400']['data_time']}")
        else:
            QMessageBox.warning(self, "警告", "未找到角色祈愿-2记录，请更新数据后重试\n也有可能没抽过")
            return

    def left_pray_list_302_change(self):
        if "武器祈愿" in self.loaded_pray_list:
            self.refreshList("武器祈愿")
            self.left_status_label.setText("状态: 已读取武器祈愿")
            self.left_update_time_label.setText(f"数据时间: {self.all_data_list[self.target_uid]['data_302']['data_time']}")
        else:
            QMessageBox.warning(self, "警告", "未找到武器祈愿记录，请更新数据后重试\n也有可能没抽过")
            return

    # Data Update Part
    def refreshData(self):
        if not os.path.exists("interact"):
            open("interact", 'w')
        if os.path.exists("requestUrl.txt"):
            os.remove("requestUrl.txt")
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

    def left_status_label_change(self, msg):
        self.left_status_label.setText(f"状态: {msg}")
        if msg == "全部列表读取完毕":
            self.left_list_label.setText("祈愿列表")
            self.clearList()
            self.pre_generate()
            self.allBtnStatusChange(True)

    # Pray List Part
    def clearList(self):
        row = self.left_pray_list.rowCount()
        for i in range(row):
            self.left_pray_list.removeRow(0)

    def refreshList(self, pray_mode):
        self.clearList()
        data_list = []
        self.left_list_label.setText(f"祈愿列表 - {pray_mode}")
        self.right_label.setText(f"分析 - {pray_mode}")
        if gachaType[pray_mode] == "100":
            data_list = self.pray_100
        if gachaType[pray_mode] == "200":
            data_list = self.pray_200
        if gachaType[pray_mode] == "301":
            data_list = self.pray_301
        if gachaType[pray_mode] == "400":
            data_list = self.pray_400
        if gachaType[pray_mode] == "302":
            data_list = self.pray_302
        for i in data_list:
            self.addRow(len(data_list), i[0], i[1], i[2])

    def setColor(self, name, row):
        if name in result_list.weapon_4_list or name in result_list.character_4_list:
            selected_color = gachaItemLevelColor[4]
        elif name in result_list.weapon_5_list or name in result_list.character_5_list:
            selected_color = gachaItemLevelColor[5]
            self.left_pray_list.item(row, 0).setForeground(QBrush(QColor(0, 0, 0)))
            self.left_pray_list.item(row, 1).setForeground(QBrush(QColor(0, 0, 0)))
            self.left_pray_list.item(row, 2).setForeground(QBrush(QColor(0, 0, 0)))
            self.left_pray_list.item(row, 3).setForeground(QBrush(QColor(0, 0, 0)))
        else:
            return
        self.left_pray_list.item(row, 0).setBackground(QBrush(selected_color))
        self.left_pray_list.item(row, 1).setBackground(QBrush(selected_color))
        self.left_pray_list.item(row, 2).setBackground(QBrush(selected_color))
        self.left_pray_list.item(row, 3).setBackground(QBrush(selected_color))

    def addRow(self, data_length, typ, name, t):
        row = self.left_pray_list.rowCount()
        self.left_pray_list.setRowCount(row + 1)
        item = QtWidgets.QTableWidgetItem()
        self.left_pray_list.setItem(row, 0, item)
        self.left_pray_list.item(row, 0).setText(str(data_length - row))
        item = QtWidgets.QTableWidgetItem()
        self.left_pray_list.setItem(row, 1, item)
        self.left_pray_list.item(row, 1).setText(typ)
        item = QtWidgets.QTableWidgetItem()
        self.left_pray_list.setItem(row, 2, item)
        self.left_pray_list.item(row, 2).setText(name)
        item = QtWidgets.QTableWidgetItem()
        self.left_pray_list.setItem(row, 3, item)
        self.left_pray_list.item(row, 3).setText(t)
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
            global gachaTarget
            gachaTarget = gachaType[key]
            data, proceed_data = [], []
            page, old_page, old_end_id, end_id = 1, 1, 0, 0
            url = gachaUrl
            url = url.split('&')
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
                    rep = requests.get(target_url).json()
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
                    self.usleep(500)
                    old_page = page
                    old_end_id = end_id
                    page += 1
                    if type(page) == int:
                        self.trigger.emit(f"正在读取第{str(page - 1)}页记录 - {key}")
                    end_id = rep["data"]["list"][-1]["id"]
                except IndexError or TypeError:
                    break
            self.trigger.emit(f"{key}读取完毕")
            if not os.path.exists(f"pray_history/{self.uid}"):
                os.mkdir(f"pray_history/{self.uid}")
            if not os.path.exists(f"pray_history/{self.uid}/original_data"):
                os.mkdir(f"pray_history/{self.uid}/original_data")
            if not os.path.exists(f"pray_history/{self.uid}/export"):
                os.mkdir(f"pray_history/{self.uid}/export")
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
