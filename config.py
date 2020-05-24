from pathlib import Path

class Config(object):
    DEBUG = True
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "thomas.stivers@gmail.com"
    MAIL_PASSWORD = "pggqduookbshamoc"
    ADMINS = ["thomas.stivers@icloud.com"]
    SECRET_KEY = "The only way to win is not to play."
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + str(Path(__file__).parent.absolute()) + ".db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
