import speech_recognition as sr
import io
import wave

class Transcription:
    def __init__(self):
        self.r = sr.Recognizer()

    def createTranscript(self, channels, width, rate, frames):
        segmentFile = io.BytesIO()
        with wave.open(segmentFile, 'wb') as f:
            f.setnchannels(channels)
            f.setsampwidth(width)
            f.setframerate(rate)
            f.writeframes(frames)
        segmentFile.seek(0)

        with sr.AudioFile(segmentFile) as source:
            audio = self.r.record(source)
        
        try:
            return self.r.recognize_google(audio)
        except sr.UnknownValueError:
            return "..."