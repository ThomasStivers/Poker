from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField, DecimalField, SelectField
from wtforms.fields.html5 import EmailField, IntegerField
from wtforms.validators import InputRequired, EqualTo, Length, NumberRange

from app import poker
from app.models import User

hand = poker.draw_hand()

class HoldCardsForm(FlaskForm):
    draw = SubmitField("Draw")
    hold_cards = SelectMultipleField(choices=zip(hand, hand))
    hold_card1 = BooleanField(hand[0])
    hold_card2 = BooleanField(hand[1])
    hold_card3 = BooleanField(hand[2])
    hold_card4 = BooleanField(hand[3])
    hold_card5 = BooleanField(hand[4])

class PlaceBetForm(FlaskForm):
    credit_choices = [
        (0.01, "1¢"),
        (0.05, "5¢"),
        (0.25, "25¢"),
        (0.5, "50¢"),
        (1, "$1"),
        (5, "$5"),
        (10, "$10"),
        (25, "$25"),
        (100, "$100"),
    ]
    buy_in = DecimalField("Buy in", validators=[InputRequired(), NumberRange(min=0.01)])
    bet_credits = IntegerField("Credits to bet", validators=[InputRequired(), NumberRange(min=1, max=5)])
    credit = SelectField("Credit value", choices=credit_choices, coerce=float, default=0.25, validators=[InputRequired()])
    bet = SubmitField("Bet")

class RegistrationForm(FlaskForm):
    email = EmailField("Email address", validators=[InputRequired()])
    username = StringField("Player name", validators=[InputRequired(), Length(3, 20)])
    password = PasswordField("Password", validators=[InputRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[InputRequired(), EqualTo("password")])
    remember_me = BooleanField("Remember Me")
    signin = SubmitField("Sign up")

    def validate_user(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different email address.")

class SigninForm(FlaskForm):
    username = StringField("Player name", validators=[InputRequired(), Length(3, 20)])
    password = PasswordField("Password", validators=[InputRequired()])
    remember_me = BooleanField("Remember Me")
    signin = SubmitField("Play")