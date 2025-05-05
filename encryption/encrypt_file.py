from cryptography.fernet import Fernet
from secrets_connections import KEY_ENCRYPTION


def encrypt_file(decrypted_path, encrypted_path):
    # using the generated key
    fernet = Fernet(KEY_ENCRYPTION)

    # opening the original file to encrypt
    with open(decrypted_path, "rb") as file:
        original = file.read()

    # encrypting the file
    encrypted = fernet.encrypt(original)

    # opening the file in write mode and
    # writing the encrypted data
    with open(encrypted_path, "wb") as encrypted_file:
        encrypted_file.write(encrypted)
