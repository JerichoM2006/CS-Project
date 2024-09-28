from PyQt5 import QtWidgets, QtCore
import sys
import warnings

from Utilities.Threadpool import Threadpool

from UserSystem.UserDetailsStorage import UserDetailsStorage
from LanguageSystem.DesktopRecording import DesktopRecording
from LanguageSystem.PrimitiveTranscription import Transcription
from LanguageSystem.TranslationAI import TranslationAI

from GUI.LoginRegisterGUI import LoginRegisterWindow

def main():

    Threadpool().initialise(10)
    UserDetailsStorage().initialise()
    DesktopRecording().initialise()
    Transcription().initialise()
    TranslationAI().initialise()

    warnings.filterwarnings("ignore", category=DeprecationWarning)

    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
            QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QtWidgets.QApplication(sys.argv)

    window = LoginRegisterWindow(app)
    window.show()
    sys.exit(app.exec_())
    

def softReset():
    UserDetailsStorage().initialise()
    UserDetailsStorage().clear()

if __name__ == "__main__":
    inp = input("Do you want to reset the database? (y/n): ")
    if inp == "y":
        softReset()
    main()