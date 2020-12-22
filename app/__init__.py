from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
app = Flask(__name__)
app.config.from_object('config.DevelopementConfig')
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login_user_page'
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

from . import views