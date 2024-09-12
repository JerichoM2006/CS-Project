import speech_recognition as sr
import DesktopRecording
import Threadpool
import io
import wave

pool = Threadpool.Threadpool(10)
recording = DesktopRecording.desktopRecording(pool)

recording.startRecording()

r = sr.Recognizer()
while True:
    test = recording.buffer.qsize()
    if recording.buffer.qsize() > 0:
        segmentFile = io.BytesIO()
        with wave.open(segmentFile, 'wb') as f:
            f.setnchannels(recording.channels)
            f.setsampwidth(recording.p.get_sample_size(recording.format))
            f.setframerate(recording.rate)
            f.writeframes(recording.getSegment())

        segmentFile.seek(0)

        with sr.AudioFile(segmentFile) as source:
            audio = r.record(source)
        
        try:
            print(r.recognize_google(audio))
        except sr.UnknownValueError:
            print("can't understand audio")


"""
r = sr.Recognizer()
with sr.AudioFile("segment.wav") as source:
    audio = r.record(source)

try:
    print(r.recognize_google(audio))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
"""