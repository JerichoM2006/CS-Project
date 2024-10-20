from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
import os

from Utilities.Singleton import Singleton

class EncryptionSystem(Singleton):
    # Encrypt a file at the given path using AES encryption
    def encrypt(self, password, path):
        # Generate a random salt
        salt = os.urandom(16)
        # Generate the key using PBKDF2
        key = PBKDF2(password, salt, dkLen=32, count=10000, prf=None)

        # Create the cipher and encrypt the file
        cipher = AES.new(key, AES.MODE_GCM)
        nonce = cipher.nonce

        with open(path, 'rb') as f:
            # Read the plaintext
            plaintext = f.read()

        ciphertext, tag = cipher.encrypt_and_digest(plaintext)

        with open(path, 'wb') as f:
            # Write the salt, nonce, tag and ciphertext to the file
            f.write(salt + nonce + tag + ciphertext)

        print("Encryption successful")

    # Decrypt a file at the given path using AES encryption
    def decrypt(self, password, path):
        # Read the salt, nonce, tag and ciphertext from the file
        with open(path, 'rb') as f:
            salt = f.read(16)
            nonce = f.read(16)
            tag = f.read(16)
            ciphertext = f.read()

        # Generate the key using PBKDF2
        key = PBKDF2(password, salt, dkLen=32, count=10000, prf=None)

        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        try:
            # Decrypt the ciphertext
            plaintext = cipher.decrypt_and_verify(ciphertext, tag)

            # Write the decrypted plaintext to the file
            with open(path, 'wb') as f:
                f.write(plaintext)
        except ValueError:
            # If the decryption fails, print an error message
            print("Decryption failed")

        print("Decryption successful")
