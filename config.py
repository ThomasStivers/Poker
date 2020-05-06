from pathlib import Path

DEBUG = True
SQLALCHEMY_DATABASE_URI = "sqlite:///" + str(Path(__file__).parent.absolute()) + "poker.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "The only way to win is not to play."