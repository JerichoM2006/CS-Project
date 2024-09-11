import asyncio
import pyaudio
import numpy as np
import asyncioInput

# Audio configuration
CHUNK = 1024  # Size of audio chunks
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1  # Number of audio channels
RATE = 44100  # Sampling rate (samples per second)

class AudioRecorder:
    def __init__(self):
        self.audio_buffer = []
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  frames_per_buffer=CHUNK)
    
    async def record(self):
        try:
            while True:
                frames = []
                for _ in range(0, int(RATE / CHUNK * 1)):  # Record for 5 seconds
                    data = self.stream.read(CHUNK)
                    frames.append(data)
                
                # Convert frames to a numpy array and add to buffer
                audio_data = b''.join(frames)
                self.audio_buffer.append(audio_data)
                print("Added audio chunk to buffer")
                await asyncio.sleep(0)  # Yield control to other tasks
        except asyncio.CancelledError:
            pass
        finally:
            self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()

async def handle_user_input(recorder: AudioRecorder):
    while True:
        user_input = await asyncioInput.asyncInput("Enter 'y' to process buffer: ")
        if user_input.lower() == 'y':
            if recorder.audio_buffer:
                audio_data = recorder.audio_buffer.pop(0)
                # Process the audio data (e.g., save to file, analyze, etc.)
                print(f"Processing audio data of length {len(audio_data)}")
            else:
                print("Buffer is empty.")
        await asyncio.sleep(0)  # Yield control to other tasks

async def main():
    # Create an instance of AudioRecorder
    recorder = AudioRecorder()

    # Create tasks for recording and handling user input
    record_task = asyncio.create_task(recorder.record())
    user_input_task = asyncio.create_task(handle_user_input(recorder))

    # Run all tasks concurrently
    await asyncio.gather(record_task, user_input_task)

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())