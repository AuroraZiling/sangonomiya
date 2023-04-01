from qfluentwidgets import NavigationWidget, MessageBox
from qframelesswindow import FramelessWindow


class MessageBoxUtil(FramelessWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
    def show(self, msg):
        w = MessageBox(
            'This is a help message',
            'You clicked a customized navigation widget. You can add more custom widgets by calling `NavigationInterface.addWidget()` 😉',
            self
        )
        w.exec()