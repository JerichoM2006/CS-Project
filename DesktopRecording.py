import pyaudio
import numpy
import asyncio

class desktopRecording:
    sound  = True
    chunk = 1024
    format = pyaudio.paInt16
    channels = 2
    rate = 44100
    secondInterval = 1
    volume = 35

    isRecording = False
    recordingTask = None
    buffer = []

    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.generateStream()

    def generateStream(self):
        deviceIndex = -1
        for i in range(self.p.get_device_count()):
            dev = self.p.get_device_info_by_index(i)
            if (dev['name'] == 'Stereo Mix (Realtek(R) Audio)' and dev['hostApi'] == 0):
                deviceIndex = dev['index']

        if (deviceIndex == -1):
            print("Stereo Mix (Realtek(R) Audio) not found")
            exit(1)
        else:
            print("Found Stereo Mix (Realtek(R) Audio) at index " + str(deviceIndex))

        self.stream = self.p.open(format=self.format,
                        channels=self.channels,
                        rate=self.rate,
                        input=self.sound,
                        input_device_index = deviceIndex,
                        frames_per_buffer=self.chunk)


    async def startRecording(self):
        print("Recording started")

        self.buffer = []
        self.isRecording = True

        if self.recordingTask == None:
            pass
            #print("Starting recording task")
            #self.recordingTask = asyncio.create_task(self.record())


    def stopRecording(self):
        print("Recording stopped")

        self.isRecording = False
        self.buffer = []

    async def getSegment(self):
        return self.buffer.pop(0)

    async def record(self):
        while True:
            if self.isRecording:
                frames = []
                for i in range(0, int(self.rate / self.chunk * self.secondInterval)):
                    data = self.stream.read(self.chunk)
                    audio_data = numpy.frombuffer(data, dtype=numpy.int16)
                    audio_data = (audio_data * self.volume).astype(numpy.int16)
                    frames.append(audio_data.tobytes())

                self.buffer.append(b''.join(frames))
            await asyncio.sleep(0)

    def __del__(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()