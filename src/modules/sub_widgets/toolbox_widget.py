import importlib
import inspect

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QLabel, QFrame

from src.modules.api.pluginManager import PluginManager

html_model = '''
<!DOCTYPE html>
<html>
  <head>
  <body style="background-color:#FAEBD7;"></body>
  </head>
  <body>
    <iframe src="https://docs.qq.com/sheet/DYkdLek9OeEFCbkNi?tab=BB08J2&u=26628077110242b8a43599ca16a40a3c"></iframe>
  </body>
</html>
'''


def get_classes(arg):
    classes = []
    cls_members = inspect.getmembers(arg, inspect.isclass)
    for (name, _) in cls_members:
        classes.append(name)
    return classes


class Toolbox(QWidget):
    def __init__(self):
        super(Toolbox, self).__init__()
        self.setWindowTitle("工具箱 / Toolbox")
        self.setFixedSize(1050, 600)
        self.base_layout = QHBoxLayout(self)
        self.global_font = QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont("assets/font.ttf"))

        # Plugin Manager
        self.plugin_manager = PluginManager("plugins")
        self.plugin_list = self.plugin_manager.get_plugin_list()
        self.plugin_name_pairs = {}

        # Sidebar
        self.side_bar = QListWidget()
        self.base_layout.addWidget(self.side_bar)

        # Content
        self.content_v_layout = QVBoxLayout()
        self.default_label = QLabel("暂无插件")
        self.content_v_layout.addWidget(self.default_label)

        self.base_layout.addLayout(self.content_v_layout)

        self.setLayout(self.base_layout)

        self.initUI()

    def initUI(self):
        self.side_bar.setFixedWidth(200)

        self.default_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.default_label.setFont(QFont(self.global_font, 25))

        self.side_bar.currentItemChanged.connect(self.plugin_changed)

        self.sidebar_init()

    def sidebar_init(self):
        loaded_plugin_list = []
        for plugin in self.plugin_list:
            loaded_plugin_list.append(importlib.import_module("plugins." + plugin.split(".")[0]))
        if loaded_plugin_list:
            self.default_label.hide()
            for plugin in range(len(loaded_plugin_list)):
                self.plugin_name_pairs[loaded_plugin_list[plugin].Plugin().plugin_name] = \
                    self.plugin_list[plugin].split(".")[0]
                self.side_bar.addItem(loaded_plugin_list[plugin].Plugin().plugin_name)
            self.side_bar.setCurrentRow(0)
        else:
            self.default_label.show()
            self.side_bar.hide()

    def plugin_changed(self):
        target_plugin = importlib.import_module("plugins." + self.plugin_name_pairs[self.side_bar.currentItem().text()])
        target_classes = target_plugin.Plugin()

        for i in list(range(self.content_v_layout.count()))[::-1]:
            item = self.content_v_layout.itemAt(i)
            self.content_v_layout.removeItem(item)
            if item.widget():
                item.widget().deleteLater()
            else:
                try:
                    item.deleteLater()
                except AttributeError:
                    pass
        content_name_label = QLabel(target_classes.plugin_name)
        content_author_label = QLabel("作者: " + target_classes.plugin_author)
        content_splitter = QFrame(self)
        content_splitter.setFrameShape(QFrame.Shape.HLine)
        content_name_label.setFont(QFont("Microsoft YaHei", 16))
        self.content_v_layout.addWidget(content_name_label)
        self.content_v_layout.addWidget(content_author_label)
        self.content_v_layout.addWidget(content_splitter)
        self.content_v_layout.addLayout(target_classes.all_layout)
        self.content_v_layout.addStretch()
