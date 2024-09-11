import DesktopRecording
import asyncio
import wave
import asyncioInput

async def generateFile(recorder):
    while True:
        if recorder.buffer.qsize() > 0:
            segment = await recorder.getSegment()
            waveFile = wave.open("output.wav", 'wb')
            waveFile.setnchannels(2)
            waveFile.setsampwidth(2)
            waveFile.setframerate(44100)
            waveFile.writeframes(segment)
            waveFile.close()
        await asyncio.sleep(0)

async def run(recorder):
    await recorder.startRecording()
    while True:
        user_input = await asyncioInput.asyncInput("Do you want to stop recording? (y/n): \n")
        if user_input == "y":
            recorder.stopRecording()
            break
        else:
            print("hi")
            print(len(recorder.buffer))
        await asyncio.sleep(0)

async def main():
    recorder = DesktopRecording.desktopRecording()

    runTask =asyncio.create_task(run(recorder))
    recordTask = asyncio.create_task(recorder.record())

    await asyncio.gather(runTask, recordTask)

asyncio.run(main())