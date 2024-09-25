from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
import os

class EncryptionSystem:
    instance = None
    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(EncryptionSystem, cls).__new__(cls)
        return cls.instance

    def encrypt(self, password, path):
        salt = os.urandom(16)
        key = PBKDF2(password, salt, dkLen=32, count=10000, prf=None)

        cipher = AES.new(key, AES.MODE_GCM)
        nonce = cipher.nonce

        with open(path, 'rb') as f:
            plaintext = f.read()

        ciphertext, tag = cipher.encrypt_and_digest(plaintext)
        with open(path, 'wb') as f:
            f.write(salt + nonce + tag + ciphertext)

        print("Encryption successful")

    def decrypt(self, password, path):
        with open(path, 'rb') as f:
            salt = f.read(16)
            nonce = f.read(16)
            tag = f.read(16)
            ciphertext = f.read()

        key = PBKDF2(password, salt, dkLen=32, count=10000, prf=None)

        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        try:
            plaintext = cipher.decrypt_and_verify(ciphertext, tag)

            with open(path, 'wb') as f:
                f.write(plaintext)
        except ValueError:
            print("Decryption failed")

        print("Decryption successful")