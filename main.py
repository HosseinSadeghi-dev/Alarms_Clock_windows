import sys
from PySide6 import QtGui
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtUiTools import QUiLoader

from stopwatch import StopWatch
from timer import Timer


class Main(QWidget):
    def __init__(self):
        super(Main, self).__init__()
        loader = QUiLoader()
        self.ui = loader.load('form.ui')

        self.stopwatch = StopWatch(self.ui)
        self.timer = Timer(self.ui)

        self.ui.setWindowIcon(QtGui.QIcon('assets/icons/icon.png'))
        self.ui.show()


if __name__ == "__main__":
    app = QApplication([])
    widget = Main()
    sys.exit(app.exec())
