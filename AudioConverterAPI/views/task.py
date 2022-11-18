from fileinput import filename
import json
import os, datetime, base64
import pathlib
import mimetypes
from google.cloud import storage
from google.cloud import pubsub_v1
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from flask import Flask
from helpers.mail import sendMail
from models import db, Users, Tasks, UsersSchema, TasksSchema
from .GCStorage import GCStorage

users_schema = UsersSchema()
tasks_schema = TasksSchema()

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'ServiceKeyGoogleCloud.json'
STORAGE_CLASSES = ('STANDARD', 'NEARLINE', 'COLDLINE', 'ARCHIVE')
working_dir = pathlib.Path.cwd()
downloads_folder = working_dir.joinpath('AudiosDownloaded')
bucket_name = 'miso-bucket-api-converter'

UPLOAD_DIRECTORY = "./audioConverterDownloaded"
ALLOWED_EXTENSIONS = {'mp3', 'acc', 'ogg', 'wav', 'wma', 'm4a'}
MESSAGE_DEFAULT = "Hello!!! this is your new converted file, thanks for use this app! "
topic_path = 'projects/misw4204-desarrollo-nube/topics/audio-converter-pub-sub'

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

app = Flask(__name__)

class TasksIdView(Resource):
    @jwt_required()
    def get(self, taskId):
        return tasks_schema.dump(Tasks.query.get_or_404(taskId))
    
    @jwt_required()
    def put(self, taskId):
        newFormat = request.args.get('newFormat')
        if newFormat not in ALLOWED_EXTENSIONS:
            return "Invalid format", 409
        task = Tasks.query.get_or_404(taskId)
        task.status = "uploaded"
        task.desiredformat=newFormat
        db.session.commit()
        return tasks_schema.dump(task)
    
    @jwt_required()
    def delete(self, taskId):
        task = Tasks.query.get_or_404(taskId)
        db.session.delete(task)
        db.session.commit()
        return '', 204

class TasksView(Resource):
    @jwt_required()
    def get(self):
        argMax = int(request.args.get('max') or 0)
        argOrder = int(request.args.get('order') or 0) #0 - asc, 1 - desc

        userId = get_jwt_identity()
        tasks = Tasks.query.filter(Tasks.iduser == userId).order_by(Tasks.id.desc() if argOrder == 1 else Tasks.id.asc())

        returnTasks = [tasks_schema.dump(task) for task in tasks]

        if(argMax > 0):
            returnTasks = returnTasks[0:argMax]

        return returnTasks
    
    @jwt_required()
    def post(self):
        userId = get_jwt_identity()
        user = Users.query.get_or_404(userId)
        fileNewFormat = request.form["newFormat"]
        fileName = request.files["file"].filename
        fileExtension = fileName.rsplit('.', 1)[1].lower()
        fileBytes = request.files["file"].read()
        if fileExtension not in ALLOWED_EXTENSIONS or fileNewFormat not in ALLOWED_EXTENSIONS:
            return "Invalid format", 409

        storage_client = storage.Client()
        gcs = GCStorage(storage_client)
        bucket_gcs = gcs.get_bucket(bucket_name)
        gcs.upload_file(bucket_gcs, fileName, fileBytes)

        task = Tasks(iduser= userId,filename = fileName,filelocation= bucket_name, status = "uploaded", originalformat=fileExtension,desiredformat=fileNewFormat, uploadeddatetime = datetime.datetime.now())
        db.session.add(task)
        db.session.commit()

        publisher = pubsub_v1.PublisherClient()
        data= fileName
        attributes = {
            "receiver":user.mail,
            "subject": 'Audio Converter',
            "message": MESSAGE_DEFAULT,
            "fileLocation": UPLOAD_DIRECTORY,
            "fileName": fileName,
            "fileExtension": fileExtension,
            "newFormat": fileNewFormat,
            "taskId": "1",
        }
        data = data.encode('utf-8')
        future = publisher.publish(topic_path,data, **attributes)
        print(future.result())

        # convertFile.delay(user.mail, 'Audio Converter', MESSAGE_DEFAULT, UPLOAD_DIRECTORY, fileName, fileExtension, fileNewFormat, task.id)

        return tasks_schema.dump(task)
