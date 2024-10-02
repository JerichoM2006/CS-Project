import io
import wave
import queue
import threading
import speech_recognition as sr

from Utilities.Threadpool import Threadpool
from Utilities.Singleton import Singleton
from LanguageSystem.DesktopRecording import DesktopRecording
from UserSystem.SettingsHandler import SettingsHandler

class Transcription(Singleton):
    def initialise(self):
        self.settingsHandler : SettingsHandler = SettingsHandler()

        self.r = sr.Recognizer()
        languageRaw = self.settingsHandler.getSetting("OriginalLanguage")
        self.language = self.settingsHandler.languageCodes[languageRaw][0]

        self.pool : Threadpool = Threadpool()
        self.recording : DesktopRecording = DesktopRecording()

        self.transcriptBuffer = queue.Queue()
        self.stopTranscript = threading.Event()

    def startGeneration(self):
        print("Transcription started")

        self.stopTranscript.clear()
        self.clearQueue(self.transcriptBuffer)

        self.pool.submit(self.generateTranscript)

    def stopGeneration(self):
        print("Transcription stopped")
        self.stopTranscript.set()
        self.pool.getResult(self.generateTranscript.__name__)

    def getTranscript(self):
        try:
            return self.transcriptBuffer.get(timeout=0.1)
        except queue.Empty:
            return None
        
    def generateTranscript(self):
        while not self.stopTranscript.is_set():
            record = self.recording.getSegment()
            if record is None:
                continue

            segmentFile = io.BytesIO()
            with wave.open(segmentFile, 'wb') as f:
                f.setnchannels(self.recording.channels)
                f.setsampwidth(self.recording.p.get_sample_size(self.recording.format))
                f.setframerate(self.recording.rate)
                f.writeframes(record)
            segmentFile.seek(0)

            with sr.AudioFile(segmentFile) as source:
                self.r.adjust_for_ambient_noise(source)
                audio = self.r.record(source)
            
            try:
                self.transcriptBuffer.put(self.r.recognize_google(audio, language=self.language))
            except sr.UnknownValueError:
                self.transcriptBuffer.put("...")

    def clearQueue(self, queue : queue.Queue):
        while not queue.empty():
            queue.get(block=True)