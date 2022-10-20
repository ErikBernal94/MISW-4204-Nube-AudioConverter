import os, datetime, base64
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from flask import Flask
from helpers.mail import sendMail

from models import db, Users, Tasks, UsersSchema, TasksSchema

users_schema = UsersSchema()
tasks_schema = TasksSchema()


UPLOAD_DIRECTORY = "../api_uploaded_files"
ALLOWED_EXTENSIONS = {'mp3', 'acc', 'ogg', 'wav', 'wma', 'm4a'}

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

app = Flask(__name__)    

class TaskView(Resource):
    @jwt_required()
    def get(self, taskId):
        return tasks_schema.dump(Tasks.query.get_or_404(taskId))
    
    @jwt_required()
    def put(self, taskId):
        if request.json["newFormat"] not in ALLOWED_EXTENSIONS:
            return "Invalid format", 409
        task = Tasks.query.get_or_404(taskId)
        task.status = "uploaded"
        task.desiredformat=request.json["newFormat"]
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
        userId = get_jwt_identity()
        tasks = Tasks.query.filter(Tasks.iduser == userId)
        return [tasks_schema.dump(task) for task in tasks]
    
    @jwt_required()
    def post(self):
        userId = get_jwt_identity()
        fileName = request.json["fileName"]
        fileExtension = fileName.rsplit('.', 1)[1].lower()
        if fileExtension not in ALLOWED_EXTENSIONS or request.json["newFormat"] not in ALLOWED_EXTENSIONS:
            return "Invalid format", 409
        base64File = request.json["file"]
        base64FileBytes = base64File.encode('utf-8')
        decoded_data = base64.decodebytes(base64FileBytes)
        with open(os.path.join(UPLOAD_DIRECTORY, fileName), "wb") as fp:
            fp.write(decoded_data)
        task = Tasks(iduser= userId,filename = fileName,filelocation= UPLOAD_DIRECTORY, status = "uploaded", originalformat=fileExtension,desiredformat=request.json["newFormat"], uploadeddatetime = datetime.datetime.now())
        db.session.add(task)
        db.session.commit()
        return tasks_schema.dump(task)
    