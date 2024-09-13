import speech_recognition as sr
import io
import wave

class Transcription:
    def __init__(self, language):
        self.r = sr.Recognizer()
        self.language = language

    def createTranscript(self, channels, width, rate, frames):
        segmentFile = io.BytesIO()
        with wave.open(segmentFile, 'wb') as f:
            f.setnchannels(channels)
            f.setsampwidth(width)
            f.setframerate(rate)
            f.writeframes(frames)
        segmentFile.seek(0)

        with sr.AudioFile(segmentFile) as source:
            self.r.adjust_for_ambient_noise(source)
            audio = self.r.record(source)
        
        try:
            return self.r.recognize_google(audio, language=self.language)
        except sr.UnknownValueError:
            return "..."