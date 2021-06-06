import time

from PySide6.QtCore import QThread


class StopWatch(QThread):
    def __init__(self, ui):
        QThread.__init__(self)
        self.h = 0
        self.m = 0
        self.s = 0
        self.ui = ui

        self.ui.btn_stopwatch_start.clicked.connect(self.start_stopwatch)
        self.ui.btn_stopwatch_pause.clicked.connect(self.pause)
        self.ui.btn_stopwatch_reset.clicked.connect(self.stop)

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
