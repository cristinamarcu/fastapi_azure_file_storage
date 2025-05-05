from azure.storage.blob import BlobServiceClient
from secrets_connections import *
import os


class AzureStorageAccessor:

    def __init__(self, container_name, connection_string):
        self.container_name = container_name
        self.connection_string = connection_string
        self.blob_service_client = BlobServiceClient.from_connection_string(
            CONNECTION_STRING
        )

    def delete_blob(self, blob_name: str):
        blob_client = self.blob_service_client.get_blob_client(
            container=self.container_name, blob=blob_name
        )
        blob_client.delete_blob()

    def download_blob_to_file(self, blob_name, file_name, file_path):
        blob_client = self.blob_service_client.get_blob_client(
            container=self.container_name, blob=blob_name
        )
        with open(file=os.path.join(file_path, file_name), mode="wb") as sample_blob:
            download_stream = blob_client.download_blob()
            sample_blob.write(download_stream.readall())

    def upload_blob_file(self, blob_name, file_name, file_path):
        container_client = self.blob_service_client.get_container_client(
            container=self.container_name
        )
        with open(file=os.path.join(file_path, file_name), mode="rb") as data:
            blob_client = container_client.upload_blob(
                name=blob_name, data=data, overwrite=True
            )
