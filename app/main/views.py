from flask import render_template, flash, redirect, request, session, url_for
from flask_login import current_user, login_required
from app import db
from app.main import bp
from app.main.forms import HoldCardsForm, PlaceBetForm, ResetUserDataForm
from app.models import Hand, User
from app.poker import (
    Card,
    cards,
    deal_replacements,
    draw_hand,
    evaluate_hand,
    pay_tables,
    payout,
)


@bp.route("/")
@bp.route("/index")
def index():
    return render_template("index.html")


@bp.route("/atm", methods=["GET", "POST"])
@login_required
def atm():
    # render_template("bet.html", form=PlaceBetForm())
    return redirect(url_for("main.bet"))


@bp.route("/bet", methods=["GET", "POST"])
@login_required
def bet():
    form = PlaceBetForm()
    [
        session.pop(key)
        for key in ["bet_credits", "credit", "hand", "holds", "replacements"]
        if key in session
    ]
    if form.validate_on_submit():
        if form.buy_in.data > 0:
            current_user.balance += float(form.buy_in.data)
        db.session.add(current_user)
        db.session.commit()
        session["credit"] = form.credit.data
        session["bet_credits"] = form.bet_credits.data
        return redirect(url_for("main.play"))
    return render_template("bet.html", title="Place Bets", form=form)


@bp.route("/play", methods=["GET", "POST"])
@login_required
def play():
    """Handles the mechanics of the video poker interface."""
    # Items in the data dictionary will be available in templates.
    data = {
        "hand": None,
        "paid": 0,
        "pay_tables": pay_tables,
        "selected_table": list(pay_tables.keys())[0],
        "title": "Play",
        "winning_hand": None,
    }
    if "bet_credits" not in session or "credit" not in session:
        flash("You must place a bet before you can play.", "info")
        return redirect(url_for("main.bet"))
    if "selected_table" not in session:
        session["selected_table"] = data["selected_table"]
    else:
        data["selected_table"] = session["selected_table"]
    data["form"] = HoldCardsForm()
    flash([data["form"].errors, data["form"].validate_on_submit()], "debug")
    if not data["form"].validate_on_submit():
        return render_template("play.html", **data)
    if "hand" not in session or "replacements" not in session:
        (session["hand"], session["replacements"]) = draw_hand()
        data["winning_hand"] = evaluate_hand(session["hand"])
        bet = session["credit"] * session["bet_credits"]
        if current_user.balance - bet < 0:
            flash("You don't have enough money to make this bet. Time to hit the ATM.", "warning")
            return redirect(url_for("main.atm"))
        current_user.balance -= bet
        current_user.bet += bet
        current_user.points += bet / 10
        db.session.add(current_user)
        db.session.commit()
        data["form"].draw.label.text = "Draw"
        data["hand"] = {card: cards[card] for card in session["hand"]}
        return render_template("play.html", **data)
    dealt = session["hand"].copy()
    if data["form"].validate_on_submit():
        session["holds"] = request.form.getlist("holds[]")
        if "holds" not in session or len(session["holds"]) == 0:
            del session["holds"]
            session["hand"] = session.pop("replacements")
            if data["form"].draw.label.text == "Draw":
                data["form"].draw.label.text = "Deal"
        else:
            session["hand"] = deal_replacements(
                session["hand"], session["holds"], session["replacements"]
            )
            del session["holds"]
            del session["replacements"]
        data["winning_hand"] = evaluate_hand(session["hand"])
        data["paid"] = payout(
            session["hand"], session["credit"], session["bet_credits"], current_user
        )
    current_hand = Hand(dealt=" ".join(dealt), hand=" ".join(session["hand"]), player=current_user)
    db.session.add(current_hand)
    db.session.commit()
    data["hand"] = {card: cards[card] for card in session["hand"]}
    return render_template("play.html", **data)


@bp.route("/user/<username>", methods=["GET", "POST"])
@login_required
def user(username):
    form = ResetUserDataForm()
    user = User.query.filter_by(username=username).first_or_404()
    if form.validate_on_submit():
        if form.points.data:
            user.points = 0
        if form.bet.data:
            user.bet = 0
        if form.wins.data:
            user.wins = 0
        if form.losses.data:
            user.losses = 0
        db.session.add(user)
        db.session.commit()
    return render_template("user.html", user=user, form=form)
