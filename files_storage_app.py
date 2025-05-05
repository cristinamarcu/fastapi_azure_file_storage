import os

from fastapi import FastAPI, UploadFile, HTTPException
from secrets_connections import *
from file_utilities.file_utilities import *
from math import floor
from compression.compress_file import *
from encryption.decrypt_file import *
from encryption.encrypt_file import *
import tempfile
from azure_storage.azure_storage_accessor import AzureStorageAccessor
from azure_database.azure_database_accessor import AzureDatabaseAccessor


temp_path = tempfile.gettempdir()
azure_blob_accessor = AzureStorageAccessor(CONTAINER_NAME, CONNECTION_STRING)
azure_database_accessor = AzureDatabaseAccessor(CONNECTION_STRING_MY_SQL)


storageapp = FastAPI()


@storageapp.get("/file/{owner_name}/{file_name}")
def get_file(owner_name: str, file_name: str):

    file_exists = azure_database_accessor.check_file_exists_database(
        owner_name, file_name
    )
    if not file_exists:
        raise HTTPException(
            status_code=404, detail="File doesn't exists in the database."
        )

    compressed_file = file_name + ".gz"
    encrypted_file = compressed_file + ".encrypted"

    blob_name = owner_name + "." + encrypted_file

    try:
        azure_blob_accessor.download_blob_to_file(blob_name, encrypted_file, temp_path)
    except Exception as e:
        raise HTTPException(
            status_code=404, detail="File doesn't exists in Azure Storage."
        )

    decrypt_file(temp_path + "\\" + encrypted_file, temp_path + "\\" + compressed_file)

    file_content = file_decompressed(temp_path + "\\" + file_name)

    if not file_content:
        raise HTTPException(status_code=500, detail="Internal server error.")

    return file_content


@storageapp.post("/uploadfile/{owner_name}/{file_name}")
async def upload_file(file: UploadFile, owner_name: str, file_name: str):

    file_exists = azure_database_accessor.check_file_exists_database(
        owner_name, file_name
    )
    if file_exists:
        raise HTTPException(status_code=409, detail="File exists in the database.")

    write_data_to_file_check = write_data_to_file(
        file.file.read(), temp_path + "\\" + file_name
    )

    if not write_data_to_file_check:
        raise HTTPException(status_code=409, detail="File exists on disk.")

    file_size = get_file_size(temp_path + "\\" + file_name)
    file_size_valid = validate_file_size(temp_path + "\\" + file_name)

    if not file_size_valid:
        raise HTTPException(status_code=409, detail="File too big.")

    compress_file(temp_path + "\\" + file_name)

    compressed_file = file_name + ".gz"
    encrypted_file = compressed_file + ".encrypted"

    encrypt_file(temp_path + "\\" + compressed_file, temp_path + "\\" + encrypted_file)

    blob_name = owner_name + "." + encrypted_file
    azure_blob_accessor.upload_blob_file(blob_name, encrypted_file, temp_path)

    azure_database_accessor.insert_new_file_database(owner_name, file_name, file_size)

    os.remove(temp_path + "\\" + encrypted_file)
    os.remove(temp_path + "\\" + compressed_file)
    os.remove(temp_path + "\\" + file_name)

    return 200


@storageapp.delete("/file/{owner_name}/{file_name}")
def delete_item(owner_name: str, file_name: str):

    file_exists = azure_database_accessor.check_file_exists_database(
        owner_name, file_name
    )
    if not file_exists:
        raise HTTPException(
            status_code=404, detail="File doesn't exists in the database."
        )

    blob_name = owner_name + "." + file_name + ".gz.encrypted"

    azure_blob_accessor.delete_blob(blob_name)

    azure_database_accessor.delete_file_from_database(owner_name, file_name)

    return 204


@storageapp.head("/file/{owner_name}/{file_name}")
def find_file(owner_name: str, file_name: str):

    file_exists = azure_database_accessor.check_file_exists_database(
        owner_name, file_name
    )
    if not file_exists:
        raise HTTPException(
            status_code=404, detail="File doesn't exists in the database."
        )

    return 200
