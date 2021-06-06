import sys
import time
from functools import partial
from win10toast import ToastNotifier


from PySide6 import QtGui
from PySide6.QtCore import QThread
from PySide6.QtWidgets import QApplication, QLabel, QMessageBox, QWidget
from PySide6.QtUiTools import QUiLoader


class StopWatch(QThread):
    def __init__(self, ui):
        QThread.__init__(self)
        self.h = 0
        self.m = 0
        self.s = 0
        self.ui = ui

        self.ui.btn_stopwatch_start.clicked.connect(self.start_stopwatch)
        self.ui.btn_stopwatch_pause.clicked.connect(self.pause)
        self.ui.btn_stopwatch_stop.clicked.connect(self.stop)

    def reset(self):
        self.h = 0
        self.m = 0
        self.s = 0

    def increase(self):

        self.s = int(self.s)
        self.m = int(self.m)
        self.h = int(self.h)

        self.s += 1
        if self.s >= 60:
            self.s = 0
            self.m += 1

        if self.m >= 60:
            self.m = 0
            self.h += 1

    def run(self):
        while True:
            self.increase()
            if int(self.h) < 10:
                self.h = f'0{self.h}'
            if int(self.m) < 10:
                self.m = f'0{self.m}'
            if int(self.s) < 10:
                self.s = f'0{self.s}'
            self.ui.lbl_stopwatch.setText(f"{self.h}:{self.m}:{self.s}")
            time.sleep(1)

    def pause(self):
        self.terminate()

    def stop(self):
        self.terminate()
        self.reset()
        self.ui.lbl_stopwatch.setText("00:00:00")

    def start_stopwatch(self):
        self.start()


class Timer(QThread):
    def __init__(self, ui):
        QThread.__init__(self)
        self.ui = ui
        self.h = self.ui.timer_h.value()
        self.m = self.ui.timer_m.value()
        self.s = self.ui.timer_s.value()
        self.f_h = self.ui.timer_h.value()
        self.f_m = self.ui.timer_m.value()
        self.f_s = self.ui.timer_s.value()

        self.toast = ToastNotifier()

        self.ui.btn_timer_start.clicked.connect(self.start_timer)
        self.ui.btn_timer_pause.clicked.connect(self.pause)
        self.ui.btn_timer_reset.clicked.connect(self.stop)

    def reset(self):
        self.h = self.f_h
        self.m = self.f_m
        self.s = self.f_s

        self.ui.timer_h.setValue(self.f_h)
        self.ui.timer_m.setValue(self.f_m)
        self.ui.timer_s.setValue(self.f_s)

    def decrease(self):

        self.s = int(self.s)
        self.m = int(self.m)
        self.h = int(self.h)

        self.s -= 1
        if self.s < 0:
            self.s = 59
            self.m -= 1

        if self.m < 0:
            self.m = 59
            self.h -= 1

    def run(self):
        while int(self.s) >= 0 and int(self.m) >= 0 and int(self.h) >= 0:
            if int(self.s) == 0 and int(self.m) == 0 and int(self.h) == 0:
                break
            self.decrease()

            # if int(self.h) < 10:
            #     self.h = f'0{self.h}'
            # if int(self.m) < 10:
            #     self.m = f'0{self.m}'
            # if int(self.s) < 10:
            #     self.s = f'0{self.s}'

            self.ui.timer_h.setValue(int(self.h))
            self.ui.timer_m.setValue(int(self.m))
            self.ui.timer_s.setValue(int(self.s))

            time.sleep(1)

        if int(self.s) == 0 and int(self.m) == 0 and int(self.h) == 0:
            self.toast.show_toast("Timer Done", "Timer That You Set Is Done",
                                  duration=20, icon_path="assets/icons/icon.ico")

    def pause(self):
        self.terminate()

    def stop(self):
        self.terminate()
        self.reset()

    def start_timer(self):
        self.h = self.ui.timer_h.value()
        self.m = self.ui.timer_m.value()
        self.s = self.ui.timer_s.value()
        self.f_h = self.ui.timer_h.value()
        self.f_m = self.ui.timer_m.value()
        self.f_s = self.ui.timer_s.value()
        self.start()


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
