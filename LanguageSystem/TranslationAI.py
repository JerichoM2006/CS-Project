import queue
import threading
from deep_translator import GoogleTranslator

from LanguageSystem.PrimitiveTranscription import Transcription
from Threadpool import Threadpool


class TranslationAI:
    translationBuffer = queue.Queue()
    stopTranslation = threading.Event()

    def __init__(self, pool : Threadpool, transciptionAI : Transcription, origLanguage, finalLanguage):
        self.transciptionAI = transciptionAI
        self.pool = pool
        self.origLanguage = origLanguage
        self.finalLanguage = finalLanguage
        self.translator = GoogleTranslator()

    def startTranslation(self):
        print("Translation started")
        self.stopTranslation = threading.Event()
        self.translationBuffer = queue.Queue()
        self.pool.submit(self.translate)

    def stopTranslation(self):
        print("Translation stopped")
        self.stopTranslation.set()
        self.pool.getResult(self.translate.__name__)

    def getTranslation(self):
        return self.translationBuffer.get(block=True)

    def translate(self):
        while not self.stopTranslation.is_set():
            transcript = self.transciptionAI.getTranscript()
            translation  = self.translator.translate(transcript, src=self.origLanguage, dest=self.finalLanguage)

            if(translation == None):
                self.translationBuffer.put("...")
            else:
                self.translationBuffer.put(translation)