import logging, datetime
from operator import or_
from flask import request
from flask_jwt_extended import jwt_required, create_access_token
from flask_restful import Resource
from sqlalchemy import or_

from models import db, Users, Tasks, UsersSchema, TasksSchema

users_schema = UsersSchema()
tasks_schema = TasksSchema()

import logging
from flask import Flask, send_from_directory

app = Flask(__name__)

class FilesView(Resource):
    @jwt_required()
    def get(self, filename):
        task = Tasks.query.filter(Tasks.filename == filename).first()
        if task is None:
            return "File not found", 409
        taskJson = tasks_schema.dump(task)
        print(taskJson)
        return send_from_directory(taskJson['filelocation'], filename, as_attachment=True)
