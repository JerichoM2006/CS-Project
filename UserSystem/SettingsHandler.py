import pathlib
import json

from Utilities.Singleton import Singleton

class SettingsHandler(Singleton):
    # A dictionary of language codes to their codes
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

    # Gets a setting from the settings file
    def getSetting(self, name):
        # Get the path to the settings file
        path = self.settingsPath = str(pathlib.Path(__file__).parent.parent.resolve()) + "/Resources/Settings.json"

        # Open the file and read the data
        with open(path, 'r') as f:
            data = json.load(f)
        
        # Return the value of the setting
        return data[name]
    
    # Sets a setting in the settings file
    def setSetting(self, name, value):
        # Get the path to the settings file
        path = self.settingsPath = str(pathlib.Path(__file__).parent.parent.resolve()) + "/Resources/Settings.json"

        # Open the file and read the data
        with open(path, 'r') as f:
            data = json.load(f)
        
        # Change the setting
        data[name] = value
        
        # Write the data back to the file
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)
