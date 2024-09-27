from PyQt5 import QtCore, QtGui, QtWidgets

from UserSystem.SettingsHandler import SettingsHandler

class SubtitleWindow(QtWidgets.QWidget):
    def __init__(self, app : QtWidgets.QApplication):
        super().__init__()

        self.settingsHandler : SettingsHandler = SettingsHandler()

        self.padding = self.settingsHandler.getSetting("SubtitlePadding")
        self.fontsize = self.settingsHandler.getSetting("SubtitleFontSize")
        self.maxWidth = self.settingsHandler.getSetting("SubtitleWidth")
        self.maxLines = self.settingsHandler.getSetting("SubtitleLines")

        self.app = app

        self.setUp()

    def setUp(self):
        self.x = int((self.app.primaryScreen().size().width()) * 0.5) - (self.maxWidth // 2)
        self.y = int(self.app.primaryScreen().size().height() - (self.maxLines * self.fontsize + 2 * self.padding) - 45)

        self.setFixedWidth(self.maxWidth)
        self.setFixedHeight(self.maxLines * self.fontsize + 2 * self.padding)

        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)
        self.setAttribute(QtCore.Qt.WA_NoChildEventsForParent, True)
        self.setWindowFlags(QtCore.Qt.SubWindow | QtCore.Qt.X11BypassWindowManagerHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.label = QtWidgets.QLabel(self)
        self.label.setText("")
        self.label.setStyleSheet(f"color: white; font-size: {self.fontsize}px;")
        self.label.setFont(QtGui.QFont("Arial", 8))
        self.label.setWordWrap(True)
        self.label.adjustSize()
        self.label.setFixedWidth(self.maxWidth - 2 * self.padding)
        self.label.move(self.padding, self.padding)

        self.move(self.x, self.y)

        self.text = ""

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(QtGui.QColor(50, 50, 50, 128)) 
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10) 
        painter.end()

    def setSubtitle(self, text):
        if self.label.height() > (self.maxLines * self.fontsize) + (self.padding * 2):
            self.text = text + " "
        else:
            self.text += text + " "

        self.label.setText(self.text)
        self.label.adjustSize()
        self.label.move(self.padding, self.padding)

    def clearSubtitles(self):
        self.label.setText(self.text)
        self.label.adjustSize()
        self.label.move(self.padding, self.padding)
        self.text = ""