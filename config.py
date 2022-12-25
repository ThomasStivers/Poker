from os import environ
from pathlib import Path


class Config(object):
    DEBUG = True
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = environ.get("MAIL_PASSWORD")
    ADMINS = ["thomas.stivers@icloud.com"]
    SECRET_KEY = environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" + str(Path(__file__).parent.absolute()) + ".db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
