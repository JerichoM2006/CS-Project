import queue
import threading
from deep_translator import GoogleTranslator

from LanguageSystem.PrimitiveTranscription import Transcription
from Utilities.Threadpool import Threadpool
from Utilities.Singleton import Singleton
from UserSystem.SettingsHandler import SettingsHandler

class TranslationAI(Singleton):
    def initialise(self):
        self.pool : Threadpool = Threadpool()
        self.transciptionAI : Transcription = Transcription()

        self.settingsHandler : SettingsHandler = SettingsHandler()

        self.origLanguageRaw = self.settingsHandler.getSetting("OriginalLanguage")
        self.finalLanguageRaw = self.settingsHandler.getSetting("FinalLanguage")
        self.origLanguage = self.settingsHandler.languageCodes[self.origLanguageRaw][1]
        self.finalLanguage = self.settingsHandler.languageCodes[self.finalLanguageRaw][1]
        self.translator = GoogleTranslator(source=self.origLanguage, target=self.finalLanguage)

        self.translationBuffer = queue.Queue()
        self.stop = threading.Event()

    def startTranslation(self):
        print("Translation started")

        self.stop.clear()
        self.clearQueue(self.translationBuffer)

        self.pool.submit(self.translate)

    def stopTranslation(self):
        print("Translation stopped")
        self.stop.set()
        self.pool.getResult(self.translate.__name__)

    def getTranslation(self):
        try:
            return self.translationBuffer.get(timeout=0.1)
        except queue.Empty:
            return None

    def translate(self):
        while not self.stop.is_set():
            transcript = self.transciptionAI.getTranscript()
            if transcript is None:
                continue

            translation  = self.translator.translate(transcript, src=self.origLanguage, dest=self.finalLanguage)

            if(translation == None):
                self.translationBuffer.put("...")
            else:
                self.translationBuffer.put(translation)

    def clearQueue(self, queue : queue.Queue):
        while not queue.empty():
            queue.get(block=True)