from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db, forms, poker
from app.models import User

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/bet", methods=["GET", "POST"])
def bet():
    form = forms.PlaceBetForm()
    if form.validate_on_submit():
        return redirect(url_for("play"))
    return render_template("bet.html", title="Place Bets", form=form)

@app.route("/play", methods=["GET", "POST"])
def play():
    form = forms.HoldCardsForm()
    if form.validate_on_submit():
        pass
    hand = poker.draw_hand()
    pay_table = poker.pay_table
    return render_template("play.html", title="Play", form=form, hand=hand, pay_table=pay_table)

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("play"))
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f"You are now registered as {form.username.data}!")
        return redirect(url_for("signin"))
    return render_template("register.html", title="Register", form=form)

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if current_user.is_authenticated:
         return redirect(url_for("play"))
    form = forms.SigninForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("signin"))
        login_user(user, remember=form.remember_me.data)
        flash(f"Welcome {user.username}")
        return redirect(url_for("play"))
    return render_template("signin.html", title="Sign in", form=form)

@app.route("/signout")
def signout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/user/<username>")
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template("user.html", user=user)