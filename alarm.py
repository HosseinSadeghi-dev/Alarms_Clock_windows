import time
from datetime import datetime

from PySide6.QtCore import QThread
from win10toast import ToastNotifier


class Alarm(QThread):
    def __init__(self, ui):
        QThread.__init__(self)
        self.ui = ui
        # self.alarm = datetime.time(str(self.h), str(self.m), str(self.s))

        self.is_active = False
        self.ui.alarm_checkbox.clicked.connect(self.check_run)

        self.toast = ToastNotifier()

    def run(self):
        while self.is_active:
            self.ui.alarm_h.setReadOnly(True)
            self.ui.alarm_m.setReadOnly(True)
            self.ui.alarm_s.setReadOnly(True)

            now = datetime.now().time()
            now = datetime.strptime(f'{now.hour}:{now.minute}:{now.second}', "%H:%M:%S").time()

            if now == self.alarm:
                print('ALARM')
                break
            else:
                print('now -> ', now)
                print('alarm -> ', self.alarm)
            time.sleep(1)

        self.toast.show_toast("Alarm", "Your Alarm's Time is Up",
                              duration=20, icon_path="assets/icons/icon.ico")
        self.check_run()

    def check_run(self):
        self.is_active = not self.is_active

        if self.is_active:
            h = self.ui.alarm_h.value()
            m = self.ui.alarm_m.value()
            s = self.ui.alarm_s.value()

            if h < 10:
                h = f'0{h}'
            if m < 10:
                m = f'0{m}'
            if s < 10:
                s = f'0{s}'

            self.alarm = datetime.strptime(f'{h}:{m}:{s}', "%H:%M:%S").time()
            self.start()
        else:
            self.ui.alarm_h.setReadOnly(False)
            self.ui.alarm_m.setReadOnly(False)
            self.ui.alarm_s.setReadOnly(False)
            self.ui.alarm_checkbox.setChecked(False)
            self.terminate()
