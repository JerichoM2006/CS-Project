from LanguageSystem.DesktopRecording import DesktopRecording
from LanguageSystem.PrimitiveTranscription import Transcription
from LanguageSystem.TranslationAI import TranslationAI
from Threadpool import Threadpool

def main():
    origLanguage = "ja-JP"
    finalLanguage = "en-US"

    pool = Threadpool(10)
    recording = DesktopRecording(pool)
    transcriptionAI = Transcription(pool, recording, origLanguage)
    translator = TranslationAI(pool, transcriptionAI, origLanguage, finalLanguage)

    recording.startRecording()
    transcriptionAI.startGeneration()
    translator.startTranslation()

    while True:
        translated = translator.getTranslation()
        print(translated, end=" ")

from GUI.LoginRegisterGUI import LoginRegisterWindow
from GUI.ControlGUI import ControlWindow
import UserSystem.UserDetailsStorage as ud
import sys
from PyQt5 import QtWidgets, QtCore
def main1():
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
            QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QtWidgets.QApplication(sys.argv)

    window = ControlWindow()
    window.show()

    sys.exit(app.exec_())
    

def softReset():
    ud.UserDetailsStorage().clear()

if __name__ == "__main__":
    main1()