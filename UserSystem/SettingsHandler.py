import pathlib
import json

from Utilities.Singleton import Singleton

class SettingsHandler(Singleton):
    languageCodes = {
        "English": ["en-US", "en"],
        "Spanish": ["es-ES", "es"],
        "French": ["fr-FR", "fr"],
        "German": ["de-DE", "de"],
        "Japanese": ["ja-JP", "ja"],
        "Chinese": ["zh-CN", "zh-CN"],
        "Filipino": ["fil-PH", "tl"],
        "Russian": ["ru-RU", "ru"],
        "Portuguese": ["pt-PT", "pt"]
    }

    def getSetting(self, name):
        path =self.settingsPath = str(pathlib.Path(__file__).parent.parent.resolve()) + "/Resources/Settings.json"

        with open(path, 'r') as f:
            data = json.load(f)
        return data[name]
    
    def setSetting(self, name, value):
        path =self.settingsPath = str(pathlib.Path(__file__).parent.parent.resolve()) + "/Resources/Settings.json"

        with open(path, 'r') as f:
            data = json.load(f)
        data[name] = value
        with open(path, 'w') as f:
            json.dump(data, f, indent=4) 