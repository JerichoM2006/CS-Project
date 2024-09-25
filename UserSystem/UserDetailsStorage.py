import sqlite3
import bcrypt
import pathlib

class UserDetailsStorage:
    instance = None
    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(UserDetailsStorage, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        userDetailPath = str(pathlib.Path(__file__).parent.parent.resolve()) + "/Databases/userStorage.db"

        self.conn = sqlite3.connect(userDetailPath)
        self.cursor = self.conn.cursor()

        self.accountPath = ""

    def signIn(self, name, password):
        self.cursor.execute('SELECT * FROM users WHERE username = ?', (name,))
        result = self.cursor.fetchall()
        for row in result:
            if bcrypt.checkpw(password.encode('utf-8'), row[2]):
                self.accountPath = str(pathlib.Path(__file__).parent.parent.resolve()) + "/Databases/" + name + ".db"
                return True
        return False

    def signUp(self, name, password):
        hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.cursor.execute('INSERT INTO users (username, hashedPassword) VALUES (?, ?)', (name, hashedPassword))
        self.conn.commit()
        self.accountPath = str(pathlib.Path(__file__).parent.parent.resolve()) + "/Databases/" + name + ".db"

    def checkUserExistence(self, name):
         self.cursor.execute('SELECT * FROM users WHERE username = ?', (name,))
         result =self.cursor.fetchone()

         if result is None:
             return False
         else:
             return True
         
    def generateUserData(self, name):
        path = str(pathlib.Path(__file__).parent.parent.resolve()) + "/Databases/" + name + ".db"
        userCon = sqlite3.connect(path)
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

    def clear(self):
        self.cursor.execute('DELETE FROM users')
        self.cursor.execute('DELETE FROM sqlite_sequence WHERE name="users"')
        self.conn.commit()

    def __del__(self):
        self.conn.close()