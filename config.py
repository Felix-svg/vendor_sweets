from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_restful import Api

app = Flask(__name__)

app.secret_key = 'd8fc08c58d204a06b70e841e3912c46e1ba4cf63c59e8f7bdfb5036a7fda2ec1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

metadata = MetaData()
db = SQLAlchemy(metadata=metadata)
migrate= Migrate(app, db)
db.init_app((app))
bcrypt = Bcrypt(app)
CORS(app)
api = Api(app)
