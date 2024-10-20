from datetime import datetime
import sqlite3
import bcrypt
import pathlib

from UserSystem.EncryptionSystem import EncryptionSystem
from Utilities.Singleton import Singleton

class UserDetailsStorage(Singleton):
    # Initialize the database connection and encryption system
    def initialise(self):
        userDetailPath = str(pathlib.Path(__file__).parent.parent.resolve()) + "/Databases/userStorage.db"
        
        # Connect to the SQLite database
        self.conn = sqlite3.connect(userDetailPath)
        self.cursor = self.conn.cursor()
        
        # Initialize account path and password
        self.accountPath = ""
        self.password = ""
        self.encryption: EncryptionSystem = EncryptionSystem()

    # Log in the user by verifying credentials
    def logIn(self, name, password):
        # Check if the username exists in the database
        self.cursor.execute('SELECT * FROM users WHERE username = ?', (name,))
        result = self.cursor.fetchall()
        
        # Validate password
        for row in result:
            if bcrypt.checkpw(password.encode('utf-8'), row[2]):
                # Set account path and decrypt user database
                self.accountPath = str(pathlib.Path(__file__).parent.parent.resolve()) + "/Databases/" + name + ".db"
                self.password = password
                self.encryption.decrypt(self.password, self.accountPath)
                
                # Close the main connection as user is logged in
                self.conn.close()
                return True
        return False

    # Sign up a new user and create their database
    def signUp(self, name, password):
        # Hash the password and insert user into the database
        hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.cursor.execute('INSERT INTO users (username, hashedPassword) VALUES (?, ?)', (name, hashedPassword))
        self.conn.commit()

        # Setup account path and password for new user
        self.accountPath = str(pathlib.Path(__file__).parent.parent.resolve()) + "/Databases/" + name + ".db"
        self.password = password

        # Generate user-specific data structure
        self.generateUserData()
        
        # Close the main connection after account creation
        self.conn.close()

    # Check if a user already exists
    def checkUserExistence(self, name):
        # Query to check user existence in the database
        self.cursor.execute('SELECT * FROM users WHERE username = ?', (name,))
        result = self.cursor.fetchone()
        
        # Return existence status
        if result is None:
            return False
        else:
            return True

    # Generate the user's database structure
    def generateUserData(self):
        # Connect to the user's personal database
        userCon = sqlite3.connect(self.accountPath)
        userCursor = userCon.cursor()

        # Create table for storing transcripts
        userCursor.execute('''
                           CREATE TABLE IF NOT EXISTS Transcripts (
                           transcriptionID INTEGER PRIMARY KEY AUTOINCREMENT, 
                           name TEXT, 
                           date TEXT
                           )
                           ''')
        
        # Create table for storing sections of transcripts
        userCursor.execute('''
                           CREATE TABLE IF NOT EXISTS Sections (
                           sectionID INTEGER PRIMARY KEY AUTOINCREMENT,
                           transcriptionID INTEGER,
                           body TEXT, 
                           date TEXT
                           )
                           ''')
        
        # Commit changes and close the user connection
        userCon.commit()
        userCon.close()

    # Insert a transcript and its sections into the database
    def insertTranscript(self, transcriptName, transcriptData):
        # Open the user-specific database
        userCon = sqlite3.connect(self.accountPath)
        userCursor = userCon.cursor()

        # Insert the transcript details
        date = str(datetime.now().strftime("%d/%m/%y"))
        userCursor.execute('INSERT INTO Transcripts (name, date) VALUES (?, ?)', (transcriptName, date))
        userCon.commit()

        # Retrieve and store the transcript ID
        transcriptID = userCursor.lastrowid
        for section in transcriptData:
            # Insert each section of the transcript
            userCursor.execute('INSERT INTO Sections (transcriptionID, body, date) VALUES (?, ?, ?)', (transcriptID, section[1], section[0]))
            userCon.commit()

        # Close the user-specific connection
        userCon.close()

    # Retrieve transcripts based on a filter
    def getTranscripts(self, filter):
        # Open the user-specific database
        userCon = sqlite3.connect(self.accountPath)
        userCursor = userCon.cursor()

        # Execute query based on filter criteria
        if filter == "":
            userCursor.execute('SELECT * FROM Transcripts')
        else:
            userCursor.execute('SELECT * FROM Transcripts WHERE name LIKE ?', ('%' + filter + '%',))

        # Fetch results and sort them by date
        result = userCursor.fetchall()
        sortedResult = sorted(result, key=lambda x: datetime.strptime(x[2], '%d/%m/%y'), reverse=True)

        # Close the user-specific connection
        userCon.close()
        return sortedResult

    # Retrieve sections of a specific transcript
    def getSections(self, transcriptID, filter):
        # Open the user-specific database
        userCon = sqlite3.connect(self.accountPath)
        userCursor = userCon.cursor()

        # Execute query for sections based on filter criteria
        if filter == "":
            userCursor.execute('SELECT * FROM Sections WHERE transcriptionID = ?', (transcriptID,))
        else:
            userCursor.execute('SELECT * FROM Sections WHERE transcriptionID = ? AND body LIKE ?', (transcriptID, '%' + filter + '%'))

        # Fetch and sort results by time
        result = userCursor.fetchall()
        sortedResult = sorted(result, key=lambda x: datetime.strptime(x[3], '%H:%M'), reverse=False)

        # Close the user-specific connection
        userCon.close()
        return sortedResult

    # Clear all user data from the main database
    def clear(self):
        # Delete all users and reset the auto-increment sequence
        self.cursor.execute('DELETE FROM users')
        self.cursor.execute('DELETE FROM sqlite_sequence WHERE name="users"')
        self.conn.commit()
