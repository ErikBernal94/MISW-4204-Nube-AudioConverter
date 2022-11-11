import os, datetime, base64
import pathlib
import mimetypes
from google.cloud import storage

class GCStorage:
    def __init__(self, storage_client):
        self.client = storage_client      

    def get_bucket(self, bucket_name):
        return self.client.get_bucket(bucket_name)

    def upload_file(self, bucket, file_path, file_content):
        file_type = file_path.split('.')[-1]
        if file_type:
            content_type = file_type
        else:
            content_type = mimetypes.guess_type(file_path)[0]
        blob = bucket.blob(file_path)
        blob.upload_from_string(file_content, content_type=content_type)
        return blob

    def upload_file_from_path(self, bucket, blob_destination, file_path):
        file_type = file_path.split('.')[-1]
        if file_type:
            content_type = file_type
        else:
            content_type = mimetypes.guess_type(file_path)[0]
        blob = bucket.blob(blob_destination)
        blob.upload_from_filename(file_path, content_type=content_type)
        return blob

    def list_blobs(self, bucket_name):
        return self.client.list_blobs(bucket_name)