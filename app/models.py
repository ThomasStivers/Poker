from datetime import datetime
from time import time

from flask import current_app
from flask_login import UserMixin
import jwt
from werkzeug.security import check_password_hash, generate_password_hash
from app import db, login
from app.poker import cards, evaluate_hand


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    joined = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(16))
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)
    points = db.Column(db.Float, default=0.0)
    bet = db.Column(db.Float, default=0.0)
    balance = db.Column(db.Float, default=0.0)
    hands = db.relationship("Hand", backref="player", lazy="dynamic")

    def __init__(
        self,
        username: str,
        email: str,
        password: str,
    ):
        self.username = username
        self.email = email
        self.set_password(password)

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        print(current_app.config["SECRET_KEY"])
        return jwt.encode(
            {"reset_password": self.id, "exp": time() + expires_in},
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )["reset_password"]
        except:
            return
        return User.query.get(id)


class Hand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dealt = db.Column(db.String(15), index=True)
    hand = db.Column(db.String(15), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column("user_id", db.ForeignKey("user.id"))

    def __repr__(self):
        return f"<Hand {self.hand}>"

    def __str__(self):
        return ", ".join([cards[card].string for card in self.hand])

    def evaluate(self, pay_table="Bonus Poker"):
        return evaluate_hand(self.hand, pay_table)
