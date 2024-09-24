from PyQt5 import QtWidgets, QtCore
import sys
import warnings

from Threadpool import Threadpool
import UserSystem.UserDetailsStorage as ud
from GUI.LoginRegisterGUI import LoginRegisterWindow
from GUI.ControlGUI import ControlWindow

def main():
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
            QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QtWidgets.QApplication(sys.argv)
    pool = Threadpool(10)

    window = ControlWindow(app, pool)
    window.show()

    sys.exit(app.exec_())
    

def softReset():
    ud.UserDetailsStorage().clear()

if __name__ == "__main__":
    main()