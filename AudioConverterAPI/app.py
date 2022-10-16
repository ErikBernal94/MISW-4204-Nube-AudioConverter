from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api

from models import db
from views import SignInView, LogInView
from views.file import FileView
from views.task import TaskView, TasksView

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
api.add_resource(SignInView, '/api/auth/signin')
api.add_resource(LogInView, '/api/auth/login')
api.add_resource(TasksView, '/api/task')
api.add_resource(TaskView, '/api/task/<int:taskId>')
api.add_resource(FileView, '/api/file/<string:filename>')

jwt = JWTManager(app)