from datetime import datetime
import sqlite3
import bcrypt
import pathlib

from UserSystem.EncryptionSystem import EncryptionSystem
from Utilities.Singleton import Singleton

class UserDetailsStorage(Singleton):
    def initialise(self):
        userDetailPath = str(pathlib.Path(__file__).parent.parent.resolve()) + "/Databases/userStorage.db"

        self.conn = sqlite3.connect(userDetailPath)
        self.cursor = self.conn.cursor()

        self.accountPath = ""
        self.password = ""
        self.encryption : EncryptionSystem = EncryptionSystem()

    def logIn(self, name, password):
        self.cursor.execute('SELECT * FROM users WHERE username = ?', (name,))
        result = self.cursor.fetchall()
        for row in result:
            if bcrypt.checkpw(password.encode('utf-8'), row[2]):
                self.accountPath = str(pathlib.Path(__file__).parent.parent.resolve()) + "/Databases/" + name + ".db"
                self.password = password

                self.encryption.decrypt(self.password, self.accountPath)
                self.conn.close()
                return True
        return False

    def signUp(self, name, password):
        hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.cursor.execute('INSERT INTO users (username, hashedPassword) VALUES (?, ?)', (name, hashedPassword))
        self.conn.commit()

        self.accountPath = str(pathlib.Path(__file__).parent.parent.resolve()) + "/Databases/" + name + ".db"
        self.password = password
        
        self.generateUserData()
        self.conn.close()

    def checkUserExistence(self, name):
         self.cursor.execute('SELECT * FROM users WHERE username = ?', (name,))
         result = self.cursor.fetchone()

         if result is None:
             return False
         else:
             return True
         
    def generateUserData(self):
        userCon = sqlite3.connect(self.accountPath)
        userCursor = userCon.cursor()

        userCursor.execute('''
                           CREATE TABLE IF NOT EXISTS Transcripts (
                           transcriptionID INTEGER PRIMARY KEY AUTOINCREMENT, 
                           name TEXT, 
                           date TEXT
                           )
                           ''')
        
        userCursor.execute('''
                           CREATE TABLE IF NOT EXISTS Sections (
                           sectionID INTEGER PRIMARY KEY AUTOINCREMENT,
                           transcriptionID INTEGER,
                           body TEXT, 
                           date TEXT
                           )
                           ''')
        
        userCon.commit()
        userCon.close()

    def insertTranscript(self, transcriptName, transcriptData):
        userCon = sqlite3.connect(self.accountPath)
        userCursor = userCon.cursor()

        date = str(datetime.now().strftime("%d:%m:%y"))
        userCursor.execute('INSERT INTO Transcripts (name, date) VALUES (?, ?)', (transcriptName, date))
        userCon.commit()

        transcriptID = userCursor.lastrowid
        for section in transcriptData:
            userCursor.execute('INSERT INTO Sections (transcriptionID, body, date) VALUES (?, ?, ?)', (transcriptID, section[1], section[0]))
            userCon.commit()

        userCon.close()


    def clear(self):
        self.cursor.execute('DELETE FROM users')
        self.cursor.execute('DELETE FROM sqlite_sequence WHERE name="users"')
        self.conn.commit()