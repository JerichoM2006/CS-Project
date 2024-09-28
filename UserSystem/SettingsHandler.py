import pathlib
import json

from Utilities.Singleton import Singleton

class SettingsHandler(Singleton):
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

