from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_enum import EnumField
import enum

db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    mail = db.Column(db.String(100))
    password = db.Column(db.String(100))
    tasks = db.relationship('Tasks', cascade='all, delete, delete-orphan')


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    iduser = db.Column(db.Integer, db.ForeignKey("users.id"))
    filename = db.Column(db.String(500))
    filelocation = db.Column(db.String(500))
    status = db.Column(db.String(30))
    originalformat = db.Column(db.String(10))
    desiredformat = db.Column(db.String(10))
    uploadeddatetime = db.Column(db.TIMESTAMP)
    processeddatetime = db.Column(db.TIMESTAMP)

class TasksSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Tasks
        include_relationships = True
        include_fk = True
        load_instance = True

class UsersSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        include_relationships = True
        
        load_instance = True
    tasks = fields.List(fields.Nested(TasksSchema()))






