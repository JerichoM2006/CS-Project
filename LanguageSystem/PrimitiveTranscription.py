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
    # Initialises the transcription
    def initialise(self):
        # Get settings
        self.settingsHandler : SettingsHandler = SettingsHandler()

        # Set up the speech recognition
        self.r = sr.Recognizer()
        languageRaw = self.settingsHandler.getSetting("OriginalLanguage")
        self.language = self.settingsHandler.languageCodes[languageRaw][0]

        # Set up the thread pool
        self.pool : Threadpool = Threadpool()

        # Set up the recording
        self.recording : DesktopRecording = DesktopRecording()

        # Set up the transcript buffer
        self.transcriptBuffer = queue.Queue()
        # Set up the stop transcript event
        self.stopTranscript = threading.Event()

    # Starts the transcription
    def startGeneration(self):
        print("Transcription started")

        # Clear the transcript buffer and start the transcription
        self.stopTranscript.clear()
        self.clearQueue(self.transcriptBuffer)

        # Submit the transcription to the thread pool
        self.pool.submit(self.generateTranscript)

    # Stops the transcription
    def stopGeneration(self):
        print("Transcription stopped")
        # Set the stop transcript event
        self.stopTranscript.set()
        # Get the result of the transcription
        self.pool.getResult(self.generateTranscript.__name__)

    # Gets the current transcript
    def getTranscript(self):
        try:
            # Get the transcript from the buffer
            return self.transcriptBuffer.get(timeout=0.1)
        except queue.Empty:
            # If the buffer is empty return None
            return None
        
    # Generates the transcript
    def generateTranscript(self):
        while not self.stopTranscript.is_set():
            # Get the segment from the recording
            record = self.recording.getSegment()
            if record is None:
                continue

            # Create a file in memory for the segment
            segmentFile = io.BytesIO()
            with wave.open(segmentFile, 'wb') as f:
                # Set the segment parameters
                f.setnchannels(self.recording.channels)
                f.setsampwidth(self.recording.p.get_sample_size(self.recording.format))
                f.setframerate(self.recording.rate)
                # Write the segment to the file
                f.writeframes(record)
            segmentFile.seek(0)

            # Create an audio file from the segment
            with sr.AudioFile(segmentFile) as source:
                # Adjust for ambient noise
                self.r.adjust_for_ambient_noise(source)
                # Record the audio
                audio = self.r.record(source)
            
            try:
                # Get the transcript from the audio
                self.transcriptBuffer.put(self.r.recognize_google(audio, language=self.language))
            except sr.UnknownValueError:
                # If the transcript can't be determined, put an ellipsis
                self.transcriptBuffer.put("...")

    # Clears the transcript buffer
    def clearQueue(self, queue : queue.Queue):
        # Empty the buffer
        while not queue.empty():
            queue.get(block=True)
