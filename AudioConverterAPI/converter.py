
import base64
import zipfile
import datetime
import mimetypes
import os
import pathlib
from google.cloud import storage
from models import db, Tasks
from helpers.mail import sendMail
from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydub import AudioSegment

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'ServiceKey_GoogleCloud.json'
STORAGE_CLASSES = ('STANDARD', 'NEARLINE', 'COLDLINE', 'ARCHIVE')

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

celery = Celery( 'tasks' , broker = 'redis://:admin@10.128.0.6:/0' )

PASSWORD ="admin"
PUBLIC_IP_ADDRESS ="34.66.98.169"
DBNAME ="postgres"
some_engine = create_engine('postgresql+psycopg2://{}:{}@{}/{}??host=/cloudsql/{}'.format('postgres', PASSWORD,PUBLIC_IP_ADDRESS, DBNAME, 'misw4204-desarrollo-nube:us-central1:audioconverter'))

# create a configured "Session" class
Session = sessionmaker(bind=some_engine)

# create a Session
session = Session()

@celery.task
def convertFile(receiver, subject, message, fileLocation, fileName, fileExtension, newFormat, taskId):
    print ('\n->Converting file : {}'.format(fileName))
    bucket_name = 'miso-bucket-api-converter'
    downloads_folder = './audioConverterDownloaded'
    # GET THE FILE FROM STORAGE
    storage_client = storage.Client()
    gcs = GCStorage(storage_client)
    bucket = gcs.get_bucket(bucket_name)
    blob = bucket.blob(fileName)
    path_download = downloads_folder+'/'+blob.name
    blob.download_to_filename(str(path_download))

    ## converting file to new format
    given_audio = AudioSegment.from_file(path_download, format=fileExtension)
    ## new file name with new format
    newFileName = fileName.rsplit('.', 1)[0].lower() + "." + newFormat 
    newFileLocation = fileLocation + "/" + newFileName                                         
    given_audio.export(newFileLocation, format=newFormat)

    gcs.upload_file_from_path(bucket, newFileName, str(newFileLocation))

    ## getting file in order to send in the  email
    fileStream = open(newFileLocation,'rb')
    newFile = fileStream.read()
    fileStream.close()
    task = session.query(Tasks).get(taskId)
    task.status = 'processed'
    task.filename = newFileName
    task.processeddatetime = datetime.datetime.now()
    session.commit()
    # enviar email
    sendMail(receiver, subject, message, newFile, fileName, fileExtension)
    print ('\n-> The file was processed and sent : {}'.format(fileName))
