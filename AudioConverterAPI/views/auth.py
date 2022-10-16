from operator import or_
from flask import request
from flask_jwt_extended import create_access_token
from flask_restful import Resource
from sqlalchemy import or_
from flask import Flask
from models import db, Users, UsersSchema, TasksSchema

users_schema = UsersSchema()
tasks_schema = TasksSchema()
app = Flask(__name__)

def getExistingUser(user, mail):
    existingUser = db.session.query(Users.id, Users.username).filter(or_(Users.username == user, Users.mail == mail)).first()
    db.session.commit()
    if existingUser is None:
        return None
    return existingUser

def loginUser(user, password):
    existingUser = db.session.query(Users.id, Users.username).filter(or_(Users.username == user, Users.password == password)).first()
    db.session.commit()
    if existingUser is None:
        return None
    return existingUser
    
class SignInView(Resource):

    def post(self):
        if(request.json["password1"] != request.json["password2"]):
            return "The passwords do not match", 409
        newUser = Users(username=request.json["username"], password=request.json["password1"], mail=request.json["mail"])
        existingUser = getExistingUser(request.json["username"], request.json["mail"])
        if existingUser is None:            
            db.session.add(newUser)
            db.session.commit()
            token_de_acceso = create_access_token(identity=newUser.id)
            db.session.commit()
            return {"message": "the user was created succesfully", "token": token_de_acceso, "id": newUser.id}
        else:
            return "The user alerady exists", 409

class LogInView(Resource):

    def post(self):
        usuario = loginUser(request.json["username"],request.json["password"])
        if usuario is None:
            return "The user does not exist", 404
        else:
            token_de_acceso = create_access_token(identity=usuario.id)
            return {"message": "Successfull login", "token": token_de_acceso}