import logging
from logging.handlers import RotatingFileHandler
import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, instance_relative_config=True)
from app import poker
app.config.from_object("config")
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "signin"
bootstrap = Bootstrap(app)
moment = Moment(app)

from app import views, models

if not app.debug:
    if not os.path.exists("logs"):
        os.mkdir("logs")
        file_handler = RotatingFileHandler("logs/poker.log", maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"))
        file_handler.setLevel(logging.INFO)
        app.logger.Addhandler(file_handler)
    app.logger.info("Poker startup")