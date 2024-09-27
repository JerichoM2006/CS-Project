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

    def initialise(self):
        self.p = pyaudio.PyAudio()
        self.generateStream()
        self.pool : Threadpool = Threadpool()

        self.stopRecord = threading.Event()
        self.buffer = queue.Queue()

        self.settingsHandler : SettingsHandler = SettingsHandler()
        self.secondInterval = self.settingsHandler.getSetting("RecordingInterval")

    def generateStream(self):
        deviceIndex = -1
        for i in range(self.p.get_device_count()):
            dev = self.p.get_device_info_by_index(i)
            if (dev['name'] == 'Stereo Mix (Realtek(R) Audio)' and dev['hostApi'] == 0):
                deviceIndex = dev['index']

        if (deviceIndex == -1):
            print("Stereo Mix (Realtek(R) Audio) not found")
            exit(1)

        self.stream = self.p.open(format=self.format,
                        channels=self.channels,
                        rate=self.rate,
                        input=self.sound,
                        input_device_index = deviceIndex,
                        frames_per_buffer=self.chunk)


    def startRecording(self):
        print("Recording started")

        self.secondInterval = self.settingsHandler.getSetting("SecondInterval")

        self.clearQueue(self.buffer)
        self.stopRecord.clear()
        
        self.pool.submit(self.record)

    def stopRecording(self):
        print("Recording stopped")
        self.stopRecord.set()
        self.pool.getResult(self.record.__name__)

    def getSegment(self):
        return self.buffer.get(block=True)
 
    def record(self):
        while not self.stopRecord.is_set():
            frames = []

            for i in range(0, int(self.rate / self.chunk * self.secondInterval)):
                data = self.stream.read(self.chunk)
                audio_data = numpy.frombuffer(data, dtype=numpy.int16)

                audio_data = (audio_data * self.volume).astype(numpy.int16)
                frames.append(audio_data.tobytes())

            self.buffer.put(b''.join(frames))

    def clearQueue(self, queue : queue.Queue):
        while not queue.empty():
            queue.get(block=True)
