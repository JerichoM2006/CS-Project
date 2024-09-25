import queue
import threading
from deep_translator import GoogleTranslator

from LanguageSystem.PrimitiveTranscription import Transcription
from Utilities.Threadpool import Threadpool
from Utilities.Singleton import Singleton

class TranslationAI(Singleton):
    def initialise(self, origLanguage, finalLanguage):
        self.pool : Threadpool = Threadpool()
        self.transciptionAI : Transcription = Transcription()

        self.origLanguage = origLanguage
        self.finalLanguage = finalLanguage
        self.translator = GoogleTranslator()

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
        return self.translationBuffer.get(block=True)

    def translate(self):
        while not self.stop.is_set():
            transcript = self.transciptionAI.getTranscript()
            translation  = self.translator.translate(transcript, src=self.origLanguage, dest=self.finalLanguage)

            if(translation == None):
                self.translationBuffer.put("...")
            else:
                self.translationBuffer.put(translation)

    def clearQueue(self, queue : queue.Queue):
        while not queue.empty():
            queue.get(block=True)