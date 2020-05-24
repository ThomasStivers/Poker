from flask import render_template, flash, redirect, request, session, url_for
from flask_login import current_user, login_required
from app import db
from app.main import bp
from app.main.forms import HoldCardsForm, PlaceBetForm
from app.models import Hand, User
from app.poker import (
    cards,
    deal_replacements,
    draw_hand,
    evaluate_hand,
    pay_table,
    payout,
)


@bp.route("/")
@bp.route("/index")
def index():
    return render_template("index.html")


@bp.route("/atm", methods=["GET", "POST"])
@login_required
def atm():
    render_template("bet.html")


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
    paid = winning_hand = None
    if "bet_credits" not in session or "credit" not in session:
        flash("You must place a bet before you can play.")
        return redirect(url_for("main.bet"))
    form = HoldCardsForm()
    if "hand" not in session or "replacements" not in session:
        (session["hand"], session["replacements"]) = draw_hand()
        winning_hand = evaluate_hand(session["hand"])
        bet = session["credit"] * session["bet_credits"]
        current_user.balance -= bet
        current_user.bet += bet
        current_user.points += bet / 10
        db.session.add(current_user)
        db.session.commit()
        form.draw.label.text = "Draw"
        hand = {card: cards[card] for card in session["hand"]}
        return render_template(
            "play.html",
            title="Play",
            form=form,
            hand=hand,
            pay_table=pay_table,
            winning_hand=winning_hand,
            paid=0,
        )
    if form.validate_on_submit():
        session["holds"] = request.form.getlist("holds[]")
        if len(session["holds"]) == 0:
            if form.draw.label.text == "Draw":
                del session["holds"]
                session["hand"] = session.pop("replacements")
                form.draw.label.text = "Deal"
        else:
            session["hand"] = deal_replacements(
                session["hand"], session["holds"], session["replacements"]
            )
            del session["holds"]
            del session["replacements"]
        winning_hand = evaluate_hand(session["hand"])
        paid = payout(
            session["hand"], session["credit"], session["bet_credits"], current_user
        )
    current_hand = Hand(hand=" ".join(session["hand"]), player=current_user)
    db.session.add(current_hand)
    db.session.commit()
    hand = {card: cards[card] for card in session["hand"]}
    return render_template(
        "play.html",
        title="Play",
        form=form,
        hand=hand,
        pay_table=pay_table,
        winning_hand=winning_hand,
        paid=paid,
    )


@bp.route("/user/<username>")
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template("user.html", user=user)
