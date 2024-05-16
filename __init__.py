from flask import Flask, flash, redirect, url_for
from authy.api import AuthyApiClient
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '1b1bdc96eb8dba64b0fc5ae1'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tables.db'
    AUTHY_API_KEY = os.environ.get('AUTHY_API_KEY')
    
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = app.config['SECRET_KEY']
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"

api = AuthyApiClient(app.config['AUTHY_API_KEY'])

login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to access this page.', 'danger')
    return redirect(url_for('login_page'))

from restaurant import routes