from PyQt6.QtWidgets import QVBoxLayout, QPushButton
import webbrowser


class Plugin:
    def __init__(self):
        super(Plugin, self).__init__()

        self.plugin_name = "角色卡池历史记录"
        self.plugin_author = "AuroraZiling"

        self.all_layout = QVBoxLayout()

        self.jump_to_gacha_history = QPushButton("角色卡池历史记录")

        self.all_layout.addWidget(self.jump_to_gacha_history)

        self.jump_to_gacha_history.clicked.connect(self.jump_to_gacha_history_clicked)

    @staticmethod
    def jump_to_gacha_history_clicked():
        webbrowser.open("https://docs.qq.com/sheet/DYkdLek9OeEFCbkNi")
