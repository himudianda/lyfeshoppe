from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf import CsrfProtect
from flask_webpack import Webpack


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
csrf = CsrfProtect()
webpack = Webpack()
