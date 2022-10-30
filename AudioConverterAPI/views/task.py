from fileinput import filename
import json
import os, datetime, base64
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from flask import Flask
from helpers.mail import sendMail
from converter import convertFile
from models import db, Users, Tasks, UsersSchema, TasksSchema

users_schema = UsersSchema()
tasks_schema = TasksSchema()


UPLOAD_DIRECTORY = "/nfs/home"
ALLOWED_EXTENSIONS = {'mp3', 'acc', 'ogg', 'wav', 'wma', 'm4a'}
MESSAGE_DEFAULT = "Hello!!! this is your new converted file, thanks for use this app! "

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

        with open(os.path.join(UPLOAD_DIRECTORY, fileName), "wb") as fp:
            fp.write(fileBytes)

        task = Tasks(iduser= userId,filename = fileName,filelocation= UPLOAD_DIRECTORY, status = "uploaded", originalformat=fileExtension,desiredformat=fileNewFormat, uploadeddatetime = datetime.datetime.now())
        db.session.add(task)
        db.session.commit()

        data = fileBytes
        base64EncodedStr = base64.b64encode(data)
        fileString =base64EncodedStr.decode('utf-8')

        convertFile.delay(user.mail, 'Audio Converter', MESSAGE_DEFAULT, UPLOAD_DIRECTORY, fileName, fileExtension, fileNewFormat, task.id)

        return tasks_schema.dump(task)
    