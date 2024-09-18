import sqlite3
import bcrypt
import os

class UserDetailsStorage:
    def __init__(self, userStoragePath):
        self.conn = sqlite3.connect(userStoragePath)
        self.cursor = self.conn.cursor()

    def signIn(self, name, password):
        self.cursor.execute('SELECT * FROM users WHERE username = ?', (name,))
        result = self.cursor.fetchall()
        for row in result:
            if bcrypt.checkpw(password.encode('utf-8'), row[2]):
                    return True
        return False

    def signUp(self, name, password):
        hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        salt = os.urandom(16)
        self.cursor.execute('INSERT INTO users (username, hashedPassword) VALUES (?, ?)', (name, hashedPassword))
        self.conn.commit()

    def clear(self):
        self.cursor.execute('DELETE FROM users')
        self.conn.commit()

    def __del__(self):
        self.conn.close()