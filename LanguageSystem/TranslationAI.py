import queue
import threading
from deep_translator import GoogleTranslator

from LanguageSystem.PrimitiveTranscription import Transcription
from Utilities.Threadpool import Threadpool
from Utilities.Singleton import Singleton
from UserSystem.SettingsHandler import SettingsHandler

class TranslationAI(Singleton):
    # Initialise the TranslationAI
    def initialise(self):
        # Set up the thread pool
        self.pool : Threadpool = Threadpool()
        # Set up the translation AI
        self.transciptionAI : Transcription = Transcription()

        # Get the settings
        self.settingsHandler : SettingsHandler = SettingsHandler()

        # Get the languages for the translation
        self.origLanguageRaw = self.settingsHandler.getSetting("OriginalLanguage")
        self.finalLanguageRaw = self.settingsHandler.getSetting("FinalLanguage")
        self.origLanguage = self.settingsHandler.languageCodes[self.origLanguageRaw][1]
        self.finalLanguage = self.settingsHandler.languageCodes[self.finalLanguageRaw][1]
        # Set up the translator
        self.translator = GoogleTranslator(source=self.origLanguage, target=self.finalLanguage)

        # Set up the translation buffer
        self.translationBuffer = queue.Queue()
        # Set up the stop event
        self.stop = threading.Event()

    # Start the translation
    def startTranslation(self):
        print("Translation started")

        # Clear the translation buffer
        self.clearQueue(self.translationBuffer)
        # Set the stop event
        self.stop.clear()
        # Submit the translation to the thread pool
        self.pool.submit(self.translate)

    # Stop the translation
    def stopTranslation(self):
        print("Translation stopped")
        # Set the stop event
        self.stop.set()
        # Get the result of the translation
        self.pool.getResult(self.translate.__name__)

    # Get the translation
    def getTranslation(self):
        try:
            return self.translationBuffer.get(timeout=0.1)
        except queue.Empty:
            return None

    # Translate the transcript
    def translate(self):
        while not self.stop.is_set():
            # Get the transcript
            transcript = self.transciptionAI.getTranscript()
            if transcript is None:
                continue

            # Translate the transcript
            translation  = self.translator.translate(transcript, src=self.origLanguage, dest=self.finalLanguage)

            # Put the translation in the translation buffer
            if(translation == None):
                self.translationBuffer.put("...")
            else:
                self.translationBuffer.put(translation)

    # Clear the translation buffer
    def clearQueue(self, queue : queue.Queue):
        while not queue.empty():
            queue.get(block=True)
