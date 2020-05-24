from flask import flash, redirect, render_template, request, url_for
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user
from app import db
from app.auth import bp
from app.auth.forms import RegistrationForm, ResetPasswordForm, ResetPasswordRequestForm, SigninForm
from app.email import send_password_reset_email
from app.models import User

@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("play"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f"You are now registered as {form.username.data}!")
        return redirect(url_for("auth.signin"))
    return render_template("auth/register.html", title="Register", form=form)

@bp.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for("main.index"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Your password has been reset.")
        return redirect(url_for("auth.signin"))
    return render_template("auth/reset_password.html", form=form)

@bp.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash("Check your email for instructions to reset your password.")
        return redirect(url_for("auth.signin"))
    return render_template("auth/reset_password_request.html", title="Reset Password", form=form)

@bp.route("/signin", methods=["GET", "POST"])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for("play"))
    form = SigninForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("auth.signin"))
        login_user(user, remember=form.remember_me.data)
        flash(f"Welcome {user.username}")
        return redirect(url_for("main.play"))
    return render_template("auth/signin.html", title="Sign in", form=form)

@bp.route("/signout")
def signout():
    logout_user()
    return redirect(url_for("main.index"))

