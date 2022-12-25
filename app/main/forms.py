from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DecimalField,
    IntegerField,
    PasswordField,
    StringField,
    SubmitField,
    SelectField,
    HiddenField,
)
from wtforms.validators import InputRequired, NumberRange
from app.poker import pay_tables


class ResetUserDataForm(FlaskForm):
    balance = BooleanField("Balance")
    points = BooleanField("Points")
    bet = BooleanField("Bet")
    wins = BooleanField("Wins")
    losses = BooleanField("Losses")
    reset = SubmitField("Clear")


class HoldCardsForm(FlaskForm):
    holds = HiddenField("holds[]")
    select_table = SelectField(
        "Pay Table",
        choices=pay_tables.keys(),
    )
    draw = SubmitField("Deal")


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
    buy_in = DecimalField("Buy in", default=0)
    bet_credits = IntegerField(
        "Credits to bet", validators=[InputRequired(), NumberRange(min=1, max=5)]
    )
    credit = SelectField(
        "Credit value",
        choices=credit_choices,
        coerce=float,
        default=0.25,
        validators=[InputRequired()],
    )
    bet = SubmitField("Bet")
