from PyQt5 import QtWidgets

from GUI.LoginRegisterGUI import LoginRegisterWindow
from GUI.ControlGUI import ControlWindow
from GUI.SettingsGUI import SettingsWindow

class ManagerWindow():
    def __init__(self, app : QtWidgets.QApplication):
        self.app = app
        self.currentWindow = None

    def switchWindow(self, window : str):
        if self.currentWindow is not None:
            self.currentWindow.close()

        if window == "LoginRegisterWindow":
            self.currentWindow = LoginRegisterWindow(self)
            self.currentWindow.show()
        elif window == "ControlWindow":
            self.currentWindow = ControlWindow(self, self.app)
            self.currentWindow.show()
        elif window == "SettingsWindow":
            self.currentWindow = SettingsWindow(self)
            self.currentWindow.show()
        else:
            print("Invalid Window")