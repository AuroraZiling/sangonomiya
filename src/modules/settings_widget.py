import json
import winreg

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QTextEdit, QLabel, QFrame, QRadioButton, \
    QMessageBox


class Settings(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("设置 / Settings")
        self.setFixedSize(490, 150)

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
        self.label_hide_new_description = QLabel("更新数据以及显示数据时，将忽略新手祈愿")
        self.hide_new_h_layout.addWidget(self.label_hide_new)
        self.hide_new_h_layout.addWidget(self.widget_hide_new)
        self.base_layout.addLayout(self.hide_new_h_layout)
        self.base_layout.addWidget(self.label_hide_new_description)

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

    def reset_proxy(self):
        try:
            winreg.SetValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings", 0, winreg.KEY_WRITE), "ProxyEnable", 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings", 0, winreg.KEY_WRITE), "ProxyServer", 0, winreg.REG_SZ, "")
            QMessageBox.information(self, "提示", "重置代理成功", QMessageBox.StandardButton.Ok)
        except Exception as e:
            QMessageBox.warning(self, "错误", "重置代理失败", QMessageBox.StandardButton.Ok)
            print(e)

    def hide_new(self):
        config = json.loads(open("config.json", 'r', encoding='utf-8').read())
        config["settings"]["hide_new"] = self.widget_hide_new.isChecked()
        open("config.json", 'w', encoding='utf-8').write(json.dumps(config, indent=4, ensure_ascii=False))
