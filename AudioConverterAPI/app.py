from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api

from models import db
from views import SignUpView, LogInView
from views.file import FilesView
from views.task import TasksIdView, TasksView

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/AudioConverter'
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)
api.add_resource(SignUpView, '/api/auth/signup')
api.add_resource(LogInView, '/api/auth/login')
api.add_resource(TasksView, '/api/tasks')
api.add_resource(TasksIdView, '/api/tasks/<int:taskId>')
api.add_resource(FilesView, '/api/files/<string:filename>')

jwt = JWTManager(app)
