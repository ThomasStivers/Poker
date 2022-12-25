from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import Email, EqualTo, InputRequired, Length, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    email = EmailField("Email address", validators=[InputRequired()])
    username = StringField("Player name", validators=[InputRequired(), Length(3, 20)])
    password = PasswordField("Password", validators=[InputRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
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


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[InputRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
    submit = SubmitField("Reset Password")


class ResetPasswordRequestForm(FlaskForm):
    email = EmailField("Email", validators=[InputRequired(), Email()])
    submit = SubmitField("Request Password Reset")


class SigninForm(FlaskForm):
    username = StringField("Player name", validators=[InputRequired(), Length(3, 20)])
    password = PasswordField("Password", validators=[InputRequired()])
    remember_me = BooleanField("Remember Me")
    signin = SubmitField("Play")
