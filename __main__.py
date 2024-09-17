from LanguageSystem.DesktopRecording import DesktopRecording
from LanguageSystem.PrimitiveTranscription import Transcription
from LanguageSystem.TranslationAI import TranslationAI
from Threadpool import Threadpool

def main():
    origLanguage = "ja-JP"
    finalLanguage = "en-US"

    pool = Threadpool(10)
    recording = DesktopRecording(pool)
    transcriptionAI = Transcription(pool, recording, origLanguage)
    translator = TranslationAI(pool, transcriptionAI, origLanguage, finalLanguage)

    recording.startRecording()
    transcriptionAI.startGeneration()
    translator.startTranslation()

    while True:
        translated = translator.getTranslation()
        print(translated, end=" ")
            

if __name__ == "__main__":
    main()