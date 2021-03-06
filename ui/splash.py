""" Sick splash screen """

import sys
import time

from PyQt5 import QtCore
from PyQt5.QtCore import QRect, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QFrame, QLabel, QProgressBar

from ui.window import App


class Worker(QThread):
    """ Loading bar for the splash (fake) """
    progress = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def run(self) -> None:
        for i in range(101):
            time.sleep(0.04)
            self.progress.emit(i)


class Splash(QWidget):
    def __init__(self, app):
        super().__init__()

        self._w = 680
        self._h = 400

        self._size = app.primaryScreen().size()
        self._display_w = self._size.width()
        self._display_h = self._size.height()

        # setting display coordinates
        self._splash_x = (self._display_w - self._w) / 2
        self._splash_y = (self._display_h - self._h) / 2

        self.val = 0
        self.worker = Worker()
        self.torpido = None

        # removing the bars
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowIcon(QIcon('./ui/assets/logo.png'))

        # setting the theme
        theme = QtCore.QFile("./ui/theme/splash.qss")
        theme.open(QtCore.QIODevice.ReadOnly)

        self.setStyleSheet(QtCore.QTextStream(theme).readAll())
        self.setMinimumSize(self._w, self._h)
        self.move(self._splash_x, self._splash_y)

        self.progress = None
        self.loading = None
        self.worker.progress.connect(self.set_progress)

        self.build_layout()
        self.show()

    def build_layout(self):
        mainLayout = QVBoxLayout(self)
        mainLayout.setSpacing(10)
        mainLayout.setContentsMargins(10, 10, 10, 10)

        dropShadowFrame = QFrame(self)
        dropShadowFrame.setFrameShape(QFrame.StyledPanel)
        dropShadowFrame.setFrameShadow(QFrame.Raised)

        font = QFont()
        font.setFamily(u"Segoe U")
        font.setPointSize(40)

        title = QLabel(dropShadowFrame)
        title.setGeometry(QRect(0, 90, 661, 61))
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setFont(font)
        title.setText("<strong>Torpido<strong>")

        font.setPointSize(12)
        description = QLabel(dropShadowFrame)
        description.setGeometry(QRect(0, 150, 661, 31))
        description.setText("A new era of video editing is starting! get ready!")
        description.setAlignment(QtCore.Qt.AlignCenter)

        self.progress = QProgressBar(dropShadowFrame)
        self.progress.setGeometry(QRect(50, 280, 561, 20))
        self.progress.setValue(0)

        font.setPointSize(10)
        self.loading = QLabel(dropShadowFrame)
        self.loading.setGeometry(QRect(0, 320, 661, 21))
        self.loading.setFont(font)
        self.loading.setAlignment(QtCore.Qt.AlignCenter)
        self.loading.setStyleSheet(u"color: #826589;")
        self.loading.setText("getting things ready ...")

        font.setPointSize(10)
        credit = QLabel(dropShadowFrame)
        credit.setText("Created by MAAS")
        credit.setGeometry(QRect(20, 350, 621, 21))
        credit.setFont(font)
        credit.setStyleSheet(u"color: rgb(98, 114, 164);")
        credit.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)

        mainLayout.addWidget(dropShadowFrame)

    def start(self):
        self.worker.start()

    def set_progress(self, val):
        self.progress.setValue(val)
        if val == 100:
            self.torpido = App()
            self.hide()


def start_splash():
    """ entry point """

    # QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_X11InitThreads)
    app = QApplication(sys.argv)
    torpido = Splash(app)
    torpido.start()

    QtCore.QTimer.singleShot(1500, lambda: torpido.loading.setText("<strong>LOADING</strong> visuals ..."))
    QtCore.QTimer.singleShot(2100, lambda: torpido.loading.setText("<strong>LOADING</strong> constants ..."))
    QtCore.QTimer.singleShot(2500, lambda: torpido.loading.setText("<strong>LOADING</strong> models ..."))
    QtCore.QTimer.singleShot(3000, lambda: torpido.loading.setText("almost done ..."))

    sys.exit(app.exec_())
