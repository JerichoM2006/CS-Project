from PyQt5 import QtWidgets

from GUI.LoginRegisterGUI import LoginRegisterWindow
from GUI.ControlGUI import ControlWindow
from GUI.SettingsGUI import SettingsWindow
from GUI.SearchingGUI import SearchingWindow
from GUI.HelpGUI import HelpWindow

class ManagerWindow():
    # ManagerWindow is the main class that handles the GUI's windows
    def __init__(self, app : QtWidgets.QApplication):
        # Initialises the ManagerWindow with the given application
        self.app = app
        self.currentWindow = None
        # The current window is set to None

    # Switches the current window to a new one
    def switchWindow(self, window : str):
        # If the current window is not None, it is closed
        if self.currentWindow is not None:
            self.currentWindow.close()

        # Switches the current window based on the given window type
        if window == "LoginRegisterWindow":
            self.currentWindow = LoginRegisterWindow(self)
            self.currentWindow.show()
        elif window == "ControlWindow":
            self.currentWindow = ControlWindow(self, self.app)
            self.currentWindow.show()
        elif window == "SettingsWindow":
            self.currentWindow = SettingsWindow(self)
            self.currentWindow.show()
        elif window == "SearchingWindow":
            self.currentWindow = SearchingWindow(self)
            self.currentWindow.show()
        elif window == "HelpWindow":
            self.currentWindow = HelpWindow(self)
            self.currentWindow.show()
        else:
            # If the window type is invalid, prints an error message
            print("Invalid Window")
