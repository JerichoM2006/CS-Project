import sqlite3
import bcrypt

class UserDetailsStorage:
    def __init__(self):
        self.conn = sqlite3.connect('userStorage.db')
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
        self.cursor.execute('INSERT INTO users (username, hashedPassword) VALUES (?, ?)', (name, hashedPassword))
        self.conn.commit()

    def clear(self):
        self.cursor.execute('DELETE FROM users')
        self.conn.commit()

    def __del__(self):
        self.conn.close()

storage = UserDetailsStorage()

while True:
    inp = input("1. Sign in\n2. Sign up\n3. Clear database\n4. Exit\n")

    if inp == "1":
        name = input("Name: ")
        password = input("Password: ")
        if storage.signIn(name, password):
            print("Sign in successful")
        else:
            print("Sign in failed")
    elif inp == "2":
        name = input("Name: ")
        password = input("Password: ")
        storage.signUp(name, password)
        print("Sign up successful")
    elif inp == "3":
        storage.clear()
        print("Database cleared")
    elif inp == "4":
        break