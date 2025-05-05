from cryptography.fernet import Fernet
from secrets_connections import KEY_ENCRYPTION


def decrypt_file(encrypted_path, decrypted_path):

    fernet = Fernet(KEY_ENCRYPTION)

    # opening the encrypted file
    with open(encrypted_path, "rb") as enc_file:
        encrypted = enc_file.read()

    # decrypting the file
    decrypted = fernet.decrypt(encrypted)

    # opening the file in write mode and
    # writing the decrypted data
    with open(decrypted_path, "wb") as dec_file:
        dec_file.write(decrypted)
