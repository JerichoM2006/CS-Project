from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class SubtitleWindow(QtWidgets.QWidget):
    def __init__(self, app : QtWidgets.QApplication):
        super().__init__()

        self.padding = 10
        self.fontsize = 12
        self.maxWidth = 800

        self.x = int((app.primaryScreen().size().width()) * 0.5) - (self.maxWidth // 2)
        self.y = int(app.primaryScreen().size().height() * 0.8)

        self.setFixedWidth(self.maxWidth)

        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)
        self.setAttribute(QtCore.Qt.WA_NoChildEventsForParent, True)
        self.setWindowFlags(QtCore.Qt.SubWindow | QtCore.Qt.X11BypassWindowManagerHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.label = QtWidgets.QLabel(self)
        self.label.setText("")
        self.label.setStyleSheet(f"color: white; font-size: {self.fontsize}px;")
        self.label.setFont(QtGui.QFont("Arial", 8))
        self.label.setWordWrap(True)
        self.label.adjustSize()

        self.resize(self.label.width() + 2 * self.padding, self.label.height() + 2 * self.padding)
        self.label.move(self.padding, self.padding)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(QtGui.QColor(50, 50, 50, 128)) 
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10) 

    def update_subtitle(self, text):
        self.label.setText(text)
        self.label.adjustSize()
        self.resize(self.label.width() + 2 * self.padding, self.label.height() + 2 * self.padding)
        self.label.move(self.padding, self.padding)
