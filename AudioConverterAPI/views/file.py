import logging, datetime
import os
import shutil
from operator import or_
from flask import request
from flask_jwt_extended import jwt_required, create_access_token
from flask_restful import Resource
from sqlalchemy import or_
from .GCStorage import GCStorage
from models import db, Users, Tasks, UsersSchema, TasksSchema
from google.cloud import storage
users_schema = UsersSchema()
tasks_schema = TasksSchema()

import logging
from flask import Flask, send_from_directory

app = Flask(__name__)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'ServiceKey_GoogleCloud.json'
STORAGE_CLASSES = ('STANDARD', 'NEARLINE', 'COLDLINE', 'ARCHIVE')
bucket_name = 'miso-bucket-api-converter'
downloads_folder = './audioConverterDownloaded'
class FilesView(Resource):
    
    @jwt_required()
    def get(self, filename):
        task = Tasks.query.filter(Tasks.filename == filename).first()
        if task is None:
            return "File not found", 409
        tasks_schema.dump(task)        
        if os.path.exists(downloads_folder):
            shutil.rmtree(downloads_folder)
        os.makedirs(downloads_folder)
        storage_client = storage.Client()
        gcs = GCStorage(storage_client)
        bucket = gcs.get_bucket(bucket_name)
        blob = bucket.blob(filename)
        path_download = downloads_folder+'/'+blob.name
        blob.download_to_filename(str(path_download))    
        return send_from_directory(downloads_folder, filename, as_attachment=True)
        
