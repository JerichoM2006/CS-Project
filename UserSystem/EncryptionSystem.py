from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
import os

class EncryptionSystem:
    def __init__(self, password):
        self.password = password

    def encrypt(self, path):
        salt = os.urandom(16)
        key = PBKDF2(self.password, salt, dkLen=32, count=10000, prf=None)

        cipher = AES.new(key, AES.MODE_GCM)
        nonce = cipher.nonce

        with open(path, 'rb') as f:
            plaintext = f.read()

        ciphertext, tag = cipher.encrypt_and_digest(plaintext)
        with open(path, 'wb') as f:
            f.write(salt + nonce + tag + ciphertext)

        print("Encryption successful")

    def decrypt(self, path):
        with open(path, 'rb') as f:
            salt = f.read(16)
            nonce = f.read(16)
            tag = f.read(16)
            ciphertext = f.read()

        key = PBKDF2(self.password, salt, dkLen=32, count=10000, prf=None)

        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        try:
            plaintext = cipher.decrypt_and_verify(ciphertext, tag)

            with open(path, 'wb') as f:
                f.write(plaintext)
        except ValueError:
            print("Decryption failed")

        print("Decryption successful")