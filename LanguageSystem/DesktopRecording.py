import pyaudio
import numpy
import queue
import threading

from Utilities.Threadpool import Threadpool
from Utilities.Singleton import Singleton
from UserSystem.SettingsHandler import SettingsHandler

class DesktopRecording(Singleton):
    sound  = True
    chunk = 1024
    format = pyaudio.paInt16
    channels = 2
    rate = 44100
    volume = 1

    # Initialises the recording
    def initialise(self):
        self.p = pyaudio.PyAudio()
        self.generateStream()
        self.pool : Threadpool = Threadpool()

        self.stopRecord = threading.Event()
        self.buffer = queue.Queue()

        self.settingsHandler : SettingsHandler = SettingsHandler()
        self.secondInterval = self.settingsHandler.getSetting("RecordingInterval")

    # Generates the stream
    def generateStream(self):
        # Finds the device index
        deviceIndex = -1
        for i in range(self.p.get_device_count()):
            dev = self.p.get_device_info_by_index(i)
            if (dev['name'] == 'Stereo Mix (Realtek(R) Audio)' and dev['hostApi'] == 0):
                deviceIndex = dev['index']

        if (deviceIndex == -1):
            print("Stereo Mix (Realtek(R) Audio) not found")
            exit(1)

        # Opens the stream
        self.stream = self.p.open(format=self.format,
                        channels=self.channels,
                        rate=self.rate,
                        input=self.sound,
                        input_device_index = deviceIndex,
                        frames_per_buffer=self.chunk)


    # Starts the recording
    def startRecording(self):
        print("Recording started")

        # Clears the buffer and starts recording
        self.clearQueue(self.buffer)
        self.stopRecord.clear()
        
        self.pool.submit(self.record)

    # Stops the recording
    def stopRecording(self):
        print("Recording stopped")
        self.stopRecord.set()
        self.pool.getResult(self.record.__name__)

    # Gets a segment of the recording
    def getSegment(self):
        try:
            return self.buffer.get(block=False)
        except queue.Empty:
            return None
 
    # Records the audio
    def record(self):
        # Records the audio until stopped
        while not self.stopRecord.is_set():
            frames = []

            # Gets the frames
            for i in range(0, int(self.rate / self.chunk * self.secondInterval)):
                if self.stopRecord.is_set():
                    return

                data = self.stream.read(self.chunk)
                audio_data = numpy.frombuffer(data, dtype=numpy.int16)

                # Adjusts the volume
                audio_data = (audio_data * self.volume).astype(numpy.int16)
                frames.append(audio_data.tobytes())

            # Puts the frames in the buffer
            self.buffer.put(b''.join(frames))

    # Clears the queue
    def clearQueue(self, queue : queue.Queue):
        # Clears the queue
        while not queue.empty():
            queue.get(block=True)
