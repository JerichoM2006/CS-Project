import io
import wave
import queue
import threading
import speech_recognition as sr

from Threadpool import Threadpool
from LanguageSystem.DesktopRecording import DesktopRecording

class Transcription:
    def __init__(self, pool : Threadpool, recording : DesktopRecording, language):
        self.r = sr.Recognizer()
        self.language = language
        self.pool = pool
        self.recording = recording

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
        return self.transcriptBuffer.get(block=True)
        
    def generateTranscript(self):
        while not self.stopTranscript.is_set():
            segmentFile = io.BytesIO()
            record = self.recording.getSegment()
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