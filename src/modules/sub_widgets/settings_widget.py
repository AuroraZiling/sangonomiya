import json
import os
import winreg

from PySide6 import QtGui
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QRadioButton, QMessageBox


def get_dir_size(dir_path):
    size = 0
    for root, dirs, files in os.walk(dir_path):
        size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
    return size


class Settings(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("设置 / Settings")
        self.setFixedSize(490, 200)

        # File About
        self.about_json = json.loads(open("config.json", "r", encoding="utf-8").read())["about"]

        # UI Design
        self.base_layout = QVBoxLayout(self)

        # Proxy
        self.reset_proxy_h_layout = QHBoxLayout(self)
        self.label_reset_proxy = QLabel("重置代理")
        self.widget_reset_proxy = QPushButton("重置")
        self.label_reset_proxy_description = QLabel("如果使用工具后出现无法上网等情况，请重置代理")
        self.reset_proxy_h_layout.addWidget(self.label_reset_proxy)
        self.reset_proxy_h_layout.addWidget(self.widget_reset_proxy)
        self.base_layout.addLayout(self.reset_proxy_h_layout)
        self.base_layout.addWidget(self.label_reset_proxy_description)

        # Hide New
        self.hide_new_h_layout = QHBoxLayout(self)
        self.label_hide_new = QLabel("停用新手祈愿读取")
        self.widget_hide_new = QRadioButton(self)
        self.label_hide_new_description = QLabel("更新数据以及显示数据时，将忽略新手祈愿 (重启后生效)")
        self.hide_new_h_layout.addWidget(self.label_hide_new)
        self.hide_new_h_layout.addWidget(self.widget_hide_new)
        self.base_layout.addLayout(self.hide_new_h_layout)
        self.base_layout.addWidget(self.label_hide_new_description)

        # Delete Cache
        self.delete_cache_h_layout = QHBoxLayout(self)
        self.label_delete_cache = QLabel("清除公告图片缓存")
        self.widget_delete_cache = QPushButton("清除")
        self.label_delete_cache_description = QLabel("清除后，打开公告时将重新下载图片")
        self.delete_cache_h_layout.addWidget(self.label_delete_cache)
        self.delete_cache_h_layout.addWidget(self.widget_delete_cache)
        self.base_layout.addLayout(self.delete_cache_h_layout)
        self.base_layout.addWidget(self.label_delete_cache_description)

        self.setLayout(self.base_layout)
        self.initUI()

    def initUI(self):
        # Reset Proxy
        self.widget_reset_proxy.setFixedWidth(100)
        self.label_reset_proxy_description.setFixedHeight(30)
        self.label_reset_proxy_description.setStyleSheet("background-color: gray; border-radius: 10px; padding: 5px;")

        self.widget_reset_proxy.clicked.connect(self.reset_proxy)
        # Hide New
        config = json.loads(open("config.json", 'r', encoding='utf-8').read())
        self.widget_hide_new.setChecked(config["settings"]["hide_new"])
        self.widget_hide_new.setFixedWidth(100)
        self.label_hide_new_description.setFixedHeight(30)
        self.label_hide_new_description.setStyleSheet("background-color: gray; border-radius: 10px; padding: 5px;")

        self.widget_hide_new.clicked.connect(self.hide_new)

        # Delete Cache
        self.label_delete_cache.setText(
            "清除公告图片缓存 ({} MB)".format(round(get_dir_size("cache") / 1024 / 1024, 2)))

        self.widget_delete_cache.setFixedWidth(100)
        self.label_delete_cache_description.setFixedHeight(30)
        self.label_delete_cache_description.setStyleSheet("background-color: gray; border-radius: 10px; padding: 5px;")

        self.widget_delete_cache.clicked.connect(self.delete_cache)

    def reset_proxy(self):
        try:
            winreg.SetValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                             "Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings", 0,
                                             winreg.KEY_WRITE), "ProxyEnable", 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                             "Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings", 0,
                                             winreg.KEY_WRITE), "ProxyServer", 0, winreg.REG_SZ, "")
            QMessageBox.information(self, "提示", "重置代理成功", QMessageBox.StandardButton.Ok)
        except Exception as e:
            QMessageBox.warning(self, "错误", "重置代理失败", QMessageBox.StandardButton.Ok)
            print(e)

    def hide_new(self):
        config = json.loads(open("config.json", 'r', encoding='utf-8').read())
        config["settings"]["hide_new"] = self.widget_hide_new.isChecked()
        open("config.json", 'w', encoding='utf-8').write(json.dumps(config, indent=4, ensure_ascii=False))

    def delete_cache(self):
        for each_file in os.listdir("./cache"):
            os.remove("./cache/" + each_file)
        QMessageBox.information(self, "提示", "缓存清除成功", QMessageBox.StandardButton.Ok)
        self.label_delete_cache.setText(
            "清除公告图片缓存 ({} MB)".format(round(get_dir_size("cache") / 1024 / 1024, 2)))

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        self.label_delete_cache.setText(
            "清除公告图片缓存 ({} MB)".format(round(get_dir_size("cache") / 1024 / 1024, 2)))
