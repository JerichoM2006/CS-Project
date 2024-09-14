import speech_recognition as sr
import io
import wave
import Threadpool
import queue
import threading
import DesktopRecording

class Transcription:
    transcriptBuffer = queue.Queue()
    stopTranscript = threading.Event()

    def __init__(self, pool : Threadpool.Threadpool, recording : DesktopRecording.desktopRecording, language):
        self.r = sr.Recognizer()
        self.language = language
        self.pool = pool
        self.recording = recording

    def startGeneration(self):
        print("Transcription started")
        self.stopTranscript = threading.Event()
        self.transcriptBuffer = queue.Queue()
        self.pool.submit(self.generateTranscript)

    def stopGeneration(self):
        print("Transcription stopped")
        self.stopTranscript.set()
        self.pool.getResult(self.generateTranscript.__name__)

    def getTranscript(self):
        return self.transcriptBuffer.get()
        
    def generateTranscript(self):
        while not self.stopTranscript.is_set():
            if self.recording.buffer.qsize() > 0:
                segmentFile = io.BytesIO()
                with wave.open(segmentFile, 'wb') as f:
                    f.setnchannels(self.recording.channels)
                    f.setsampwidth(self.recording.p.get_sample_size(self.recording.format))
                    f.setframerate(self.recording.rate)
                    f.writeframes(self.recording.getSegment())
                segmentFile.seek(0)

                with sr.AudioFile(segmentFile) as source:
                    self.r.adjust_for_ambient_noise(source)
                    audio = self.r.record(source)
                
                try:
                    self.transcriptBuffer.put(self.r.recognize_google(audio, language=self.language))
                except sr.UnknownValueError:
                    self.transcriptBuffer.put("...")