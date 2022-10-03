import json
import webbrowser

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QTextEdit, QLabel


class About(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("关于 / About")
        self.setFixedSize(490, 500)

        # File About
        self.about_json = json.loads(open("config.json", "r", encoding="utf-8").read())["about"]

        # UI Design
        self.base_layout = QVBoxLayout(self)
        self.content_change_h_layout = QHBoxLayout()
        self.link_h_layout = QHBoxLayout()

        self.software_label = QLabel("Genshin Pray Export")
        self.software_version = QLabel(self.about_json["version"])
        self.author_qq_label = QLabel("QQ: 2935876049")
        self.author_mail = QLabel("Mail: 2935876049@qq.com")

        self.github_repo_btn = QPushButton("GitHub Repo")
        self.document_btn = QPushButton("GPE Document")
        self.link_h_layout.addWidget(self.github_repo_btn)
        self.link_h_layout.addWidget(self.document_btn)

        self.content_textEdit = QTextEdit(self)
        self.base_layout.addWidget(self.software_label)
        self.base_layout.addWidget(self.software_version)
        self.base_layout.addWidget(self.author_qq_label)
        self.base_layout.addWidget(self.author_mail)
        self.base_layout.addLayout(self.link_h_layout)
        self.base_layout.addWidget(self.content_textEdit)

        self.content_license_btn = QPushButton("许可证 / License")
        self.content_open_source_btn = QPushButton("开源许可 / Open Source")
        self.content_change_h_layout.addWidget(self.content_license_btn)
        self.content_change_h_layout.addWidget(self.content_open_source_btn)

        self.base_layout.addLayout(self.base_layout)
        self.base_layout.addLayout(self.content_change_h_layout)

        self.setLayout(self.base_layout)
        self.initUI()

    def initUI(self):
        self.base_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.software_label.setFont(QFont("Microsoft YaHei", 16))
        self.software_label.setFixedWidth(500)
        self.software_version.setFont(QFont("Microsoft YaHei", 10))
        self.content_textEdit.setReadOnly(True)
        self.content_textEdit.setFont(QFont("Microsoft YaHei", 10))
        self.content_textEdit.setText(open("modules/sub_widgets/about/license", "r", encoding="utf-8").read())

        self.github_repo_btn.clicked.connect(self.general_open_github_repo)
        self.document_btn.clicked.connect(self.open_document)
        self.content_license_btn.clicked.connect(self.load_license)
        self.content_open_source_btn.clicked.connect(self.load_open_source)

    @staticmethod
    def general_open_github_repo():
        webbrowser.open("https://github.com/AuroraZiling/genshin-pray-export")

    @staticmethod
    def open_document():
        webbrowser.open("https://auroraziling.github.io/genshin-pray-export/")

    def load_license(self):
        self.content_textEdit.setText(open("modules/sub_widgets/about/license", "r", encoding="utf-8").read())

    def load_open_source(self):
        self.content_textEdit.setText(open("modules/sub_widgets/about/open_source", "r", encoding="utf-8").read())
