from Threadpool import Threadpool
from GUI.LoginRegisterGUI import LoginRegisterWindow
from GUI.ControlGUI import ControlWindow
import UserSystem.UserDetailsStorage as ud
import sys
from PyQt5 import QtWidgets, QtCore
def main():
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
            QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QtWidgets.QApplication(sys.argv)
    pool = Threadpool(10)

    window = ControlWindow(pool)
    window.show()

    sys.exit(app.exec_())
    

def softReset():
    ud.UserDetailsStorage().clear()

if __name__ == "__main__":
    main1()