from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api

from models import db
from views import SignUpView, LogInView
from views.file import FilesView
from views.task import TasksIdView, TasksView

app = Flask(__name__)

# conexion a cloud

PASSWORD ="admin"
PUBLIC_IP_ADDRESS ="34.66.98.169"
DBNAME ="audioconverter"
 
# configuration
# app.config["SECRET_KEY"] = "yoursecretkey"
# app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql + mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket =/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True
 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+pg8000://{}:{}@{}/{}'.format('postgres', PASSWORD, PUBLIC_IP_ADDRESS, DBNAME)
# postgresql+pg8000://<db_user>:<db_pass>@/<db_name>
        #                         ?unix_sock=<INSTANCE_UNIX_SOCKET>/.s.PGSQL.5432
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+pg8000://{}:{}@/{}?unix_sock={}/.s.PGSQL.5432'.format('postgres', PASSWORD, DBNAME, 'misw4204-desarrollo-nube:us-central1:audioconverter')
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
