from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QListWidget

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


class Toolbox(QWidget):
    def __init__(self):
        super(Toolbox, self).__init__()
        self.setWindowTitle("工具箱 / Toolbox")
        self.setFixedSize(1050, 600)
        self.base_layout = QHBoxLayout(self)
        self.global_font = "Microsoft YaHei"

        # Sidebar
        self.side_bar = QListWidget()
        self.base_layout.addWidget(self.side_bar)

        # Content
        self.content_v_layout = QVBoxLayout()
        self.content = QWebEngineView()
        self.content_v_layout.addWidget(self.content)

        self.base_layout.addLayout(self.content_v_layout)

        self.setLayout(self.base_layout)

        self.initUI()

    def initUI(self):
        self.side_bar.setFixedWidth(200)
