from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES

class EncryptionSystem:
    def __init__(self, password, salt):
        #derive aes key from password and salt
        self.key = PBKDF2(password, salt, dkLen=32, count=10000, prf=None)

    def encrypt(self):
        pass

    def decrypt(self):
        pass