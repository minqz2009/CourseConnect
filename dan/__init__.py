from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager, current_user

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'danger'
login_manager.login_message = "You must be logged in to access that page"

from dan import views, models

@login_manager.user_loader
def load_user(id):
    if models.User.query.get(id):
        return models.User.query.get(id)

