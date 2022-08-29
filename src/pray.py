# -*- coding:utf-8 -*-
import getpass
import os
import pickle
import subprocess
import time
import qdarkstyle
import sys
import requests
from PyQt6.QtWidgets import QWidget, QMainWindow, QHBoxLayout, QTableWidget, QPushButton, QApplication, QVBoxLayout, \
    QMessageBox, QAbstractItemView, QHeaderView, QLabel
from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont

gachaUrl = ""
gachaType = {"新手祈愿": "100", "常驻祈愿": "200", "角色祈愿": "301", "武器祈愿": "302"}
gachaTarget = ""

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
        self.data_dir = f"C:/Users/{getpass.getuser()}/AppData/LocalLow/miHoYo/原神"
        self.setWindowTitle("Genshin Pray Export")
        self.setFixedSize(510, 600)
        self.setStyleSheet(qdarkstyle.load_stylesheet())

        self.loaded_pray_list = []
        self.pray_100, self.pray_200, self.pray_301, self.pray_302 = None, None, None, None

        # Multi-process
        self.get_pray_list_thread = PrayListThread()

        # UI Design
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.all_layout = QVBoxLayout(self)

        self.top_layout = QHBoxLayout(self)
        self.list_label = QLabel("祈愿记录")
        self.refresh_btn = QPushButton("更新数据")
        self.export_btn = QPushButton("导出")
        self.settings_btn = QPushButton("设置")
        self.top_layout.addWidget(self.list_label)
        self.top_layout.addWidget(self.refresh_btn)
        self.top_layout.addWidget(self.export_btn)
        self.top_layout.addWidget(self.settings_btn)
        self.all_layout.addLayout(self.top_layout)

        self.pray_list = QTableWidget(self)
        self.all_layout.addWidget(self.pray_list)

        self.pray_mode_h_layout = QHBoxLayout(self)
        self.pray_mode_100_btn = QPushButton("新手祈愿")
        self.pray_mode_200_btn = QPushButton("常驻祈愿")
        self.pray_mode_301_btn = QPushButton("角色祈愿")
        self.pray_mode_302_btn = QPushButton("武器祈愿")
        self.pray_mode_h_layout.addWidget(self.pray_mode_100_btn)
        self.pray_mode_h_layout.addWidget(self.pray_mode_200_btn)
        self.pray_mode_h_layout.addWidget(self.pray_mode_301_btn)
        self.pray_mode_h_layout.addWidget(self.pray_mode_302_btn)
        self.all_layout.addLayout(self.pray_mode_h_layout)

        self.bottom_h_layout = QHBoxLayout(self)
        self.status_label = QLabel("状态: 无")
        self.current_uid_label = QLabel("UID: 未知")
        self.update_time_label = QLabel("数据时间: 未知")
        self.bottom_h_layout.addWidget(self.status_label)
        self.bottom_h_layout.addWidget(self.current_uid_label)
        self.bottom_h_layout.addWidget(self.update_time_label)
        self.all_layout.addLayout(self.bottom_h_layout)

        self.widget.setLayout(self.all_layout)
        self.pre_generate()
        self.file_check()
        self.initUI()
        self.debug_code()

    def pre_generate(self):
        for each_dir in os.listdir("pray_history"):
            self.all_data_list.update({each_dir: {"data_100": {"data": [], "data_time": ""},
                                                  "data_200": {"data": [], "data_time": ""},
                                                  "data_301": {"data": [], "data_time": ""},
                                                  "data_302": {"data": [], "data_time": ""}}})
            if os.path.exists(f"pray_history/{each_dir}/100.pickle"):
                data_100 = pickle.load(open(f"pray_history/{each_dir}/100.pickle", "rb"))
                data_time_100 = time.strftime("%Y-%m-%d %H:%M:%S",
                                              time.localtime((os.path.getmtime(f"pray_history/{each_dir}/100.pickle"))))
                self.all_data_list[each_dir]["data_100"]["data"] = data_100
                self.loaded_pray_list.append("新手祈愿")
                self.pray_100 = data_100
                self.all_data_list[each_dir]["data_100"]["data_time"] = data_time_100
            if os.path.exists(f"pray_history/{each_dir}/200.pickle"):
                data_200 = pickle.load(open(f"pray_history/{each_dir}/200.pickle", "rb"))
                data_time_200 = time.strftime("%Y-%m-%d %H:%M:%S",
                                              time.localtime((os.path.getmtime(f"pray_history/{each_dir}/200.pickle"))))
                self.all_data_list[each_dir]["data_200"]["data"] = data_200
                self.loaded_pray_list.append("常驻祈愿")
                self.pray_200 = data_200
                self.all_data_list[each_dir]["data_200"]["data_time"] = data_time_200
            if os.path.exists(f"pray_history/{each_dir}/301.pickle"):
                data_301 = pickle.load(open(f"pray_history/{each_dir}/301.pickle", "rb"))
                data_time_301 = time.strftime("%Y-%m-%d %H:%M:%S",
                                              time.localtime((os.path.getmtime(f"pray_history/{each_dir}/301.pickle"))))
                self.all_data_list[each_dir]["data_301"]["data"] = data_301
                self.loaded_pray_list.append("角色祈愿")
                self.pray_301 = data_301
                self.all_data_list[each_dir]["data_301"]["data_time"] = data_time_301
            if os.path.exists(f"pray_history/{each_dir}/302.pickle"):
                data_302 = pickle.load(open(f"pray_history/{each_dir}/302.pickle", "rb"))
                data_time_302 = time.strftime("%Y-%m-%d %H:%M:%S",
                                              time.localtime((os.path.getmtime(f"pray_history/{each_dir}/302.pickle"))))
                self.all_data_list[each_dir]["data_302"]["data"] = data_302
                self.loaded_pray_list.append("武器祈愿")
                self.pray_302 = data_302
                self.all_data_list[each_dir]["data_302"]["data_time"] = data_time_302
        # Pre: 多UID支持预备
        if self.all_data_list:
            self.target_uid = list(self.all_data_list.keys())[0]
            self.current_uid_label.setText(f"UID: {self.target_uid}")

    def file_check(self):
        if not os.path.exists("assets"):
            QMessageBox.critical(self, "错误", "未找到必要模块，请检查目录(assets)是否存在")
            sys.exit()
        if not os.path.exists("modules"):
            QMessageBox.critical(self, "错误", "未找到必要模块，请检查目录(modules)是否存在")
            sys.exit()
        if not os.path.exists("pray_history"):
            os.mkdir("pray_history")

    def debug_code(self):
        pass

    # UI Part
    def allBtnStatusChange(self, is_enabled: bool):
        self.pray_mode_100_btn.setEnabled(is_enabled)
        self.pray_mode_200_btn.setEnabled(is_enabled)
        self.pray_mode_301_btn.setEnabled(is_enabled)
        self.pray_mode_302_btn.setEnabled(is_enabled)
        self.refresh_btn.setEnabled(is_enabled)
        # Locked
        # self.export_btn.setEnabled(is_enabled)
        # self.settings_btn.setEnabled(is_enabled)

    def initUI(self):
        # Top Layout
        self.list_label.setFont(QFont("Microsoft YaHei", 13))
        self.refresh_btn.setFixedWidth(90)
        self.export_btn.setFixedWidth(90)
        self.settings_btn.setFixedWidth(90)
        self.export_btn.setEnabled(False)  # Locked
        self.settings_btn.setEnabled(False)  # Locked

        self.refresh_btn.clicked.connect(self.refreshData)
        # Pray List
        self.pray_list.setColumnCount(3)
        self.pray_list.setHorizontalHeaderLabels(["类型", "名称", "时间"])
        self.pray_list.setColumnWidth(0, 60)
        self.pray_list.setColumnWidth(1, 180)
        self.pray_list.setColumnWidth(2, 253)
        self.pray_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.pray_list.setShowGrid(False)
        self.pray_list.verticalHeader().setHidden(True)
        self.pray_list.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.pray_list.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.pray_list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # Pray Mode Layout
        self.pray_mode_100_btn.clicked.connect(self.pray_list_100_change)
        self.pray_mode_200_btn.clicked.connect(self.pray_list_200_change)
        self.pray_mode_301_btn.clicked.connect(self.pray_list_301_change)
        self.pray_mode_302_btn.clicked.connect(self.pray_list_302_change)

    # Pray Mode Part
    def pray_list_100_change(self):
        if "新手祈愿" in self.loaded_pray_list:
            self.refreshList("新手祈愿")
            self.status_label.setText("状态: 已读取新手祈愿")
            self.update_time_label.setText(f"数据时间: {self.all_data_list[self.target_uid]['data_100']['data_time']}")
        else:
            QMessageBox.warning(self, "警告", "未找到新手祈愿记录，请更新数据后重试\n也有可能没抽过")
            return

    def pray_list_200_change(self):
        if "常驻祈愿" in self.loaded_pray_list:
            self.refreshList("常驻祈愿")
            self.status_label.setText("状态: 已读取常驻祈愿")
            self.update_time_label.setText(f"数据时间: {self.all_data_list[self.target_uid]['data_200']['data_time']}")
        else:
            QMessageBox.warning(self, "警告", "未找到常驻祈愿记录，请更新数据后重试\n也有可能没抽过")
            return

    def pray_list_301_change(self):
        if "角色祈愿" in self.loaded_pray_list:
            self.refreshList("角色祈愿")
            self.status_label.setText("状态: 已读取角色祈愿")
            self.update_time_label.setText(f"数据时间: {self.all_data_list[self.target_uid]['data_301']['data_time']}")
        else:
            QMessageBox.warning(self, "警告", "未找到角色祈愿记录，请更新数据后重试\n也有可能没抽过")
            return

    def pray_list_302_change(self):
        if "武器祈愿" in self.loaded_pray_list:
            self.refreshList("武器祈愿")
            self.status_label.setText("状态: 已读取武器祈愿")
            self.update_time_label.setText(f"数据时间: {self.all_data_list[self.target_uid]['data_302']['data_time']}")
        else:
            QMessageBox.warning(self, "警告", "未找到武器祈愿记录，请更新数据后重试\n也有可能没抽过")
            return

    # Refresh Data Part
    def refreshData(self):
        if not os.path.exists("python_interact"):
            open("python_interact", 'w')
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
        self.pray_list_thread_execute()

    # Pray List Thread
    def pray_list_thread_execute(self):
        self.allBtnStatusChange(False)
        self.get_pray_list_thread.start()
        self.get_pray_list_thread.trigger.connect(self.status_label_change)

    def status_label_change(self, msg):
        self.status_label.setText(f"状态: {msg}")
        if msg == "全部列表读取完毕":
            self.list_label.setText("祈愿列表")
            self.clearList()
            self.allBtnStatusChange(True)

    # Pray List Part

    def clearList(self):
        row = self.pray_list.rowCount()
        for i in range(row):
            self.pray_list.removeRow(0)

    def refreshList(self, pray_mode):
        self.clearList()
        data_list = []
        self.list_label.setText(f"祈愿列表 - {pray_mode}")
        if gachaType[pray_mode] == "100":
            data_list = self.pray_100
        if gachaType[pray_mode] == "200":
            data_list = self.pray_200
        if gachaType[pray_mode] == "301":
            data_list = self.pray_301
        if gachaType[pray_mode] == "302":
            data_list = self.pray_302
        for i in data_list:
            self.addRow(i[0], i[1], i[2])

    def addRow(self, typ, name, t):
        row = self.pray_list.rowCount()
        self.pray_list.setRowCount(row + 1)
        item = QtWidgets.QTableWidgetItem()
        self.pray_list.setItem(row, 0, item)
        self.pray_list.item(row, 0).setText(typ)
        item = QtWidgets.QTableWidgetItem()
        self.pray_list.setItem(row, 1, item)
        self.pray_list.item(row, 1).setText(name)
        item = QtWidgets.QTableWidgetItem()
        self.pray_list.setItem(row, 2, item)
        self.pray_list.item(row, 2).setText(t)
        self.pray_list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.pray_list.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)


class PrayListThread(QThread):
    trigger = pyqtSignal(str)

    def __init__(self, parent=None):
        super(PrayListThread, self).__init__(parent)
        self.uid = ""

    def run(self):
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
            self.uid = rep['data']["list"][0]['uid']
            while True:
                try:
                    target_url = target_url.replace(f"page={old_page}", f"page={page}").replace(f"end_id={old_end_id}",
                                                                                                f"end_id={end_id}")
                    rep = requests.get(target_url).json()
                    if rep["data"] is None:
                        break
                    tmp = rep["data"]["list"]
                    for i in range(len(tmp)):
                        proceed_data.append([tmp[i]['item_type'], tmp[i]['name'], tmp[i]['time']])
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
            with open(f'pray_history/{self.uid}/{gachaTarget}.pickle', 'wb') as f:
                pickle.dump(proceed_data, f)
        self.trigger.emit("全部列表读取完毕")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(os.path.join(basedir, 'assets/icon.ico')))
    demo = MainForm()
    demo.show()
    sys.exit(app.exec())
