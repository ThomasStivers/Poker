from collections import namedtuple, Counter
from itertools import product
import random
import time

from app import db

Card = namedtuple("card", ["face", "suit", "string"])
faces = "2 3 4 5 6 7 8 9 10 Jack Queen King Ace".split(" ")
suits = "Clubs Diamonds Hearts Spades".split(" ")
cards = [
    Card(face=c[0], suit=c[1], string=f"{c[0]} of {c[1]}")
    for c in product(faces, suits)
]
keys = [
    "".join(card)
    for card in list(
        product([f[0] if f != "10" else "T" for f in faces], [s[0] for s in suits])
    )
]
cards = dict(zip(keys, cards))

pay_table = {
    "name": "Jacks or Better",
    "Royal flush.": 800,
    "straight flush.": 50,
    "Four of a kind.": 25,
    "Full house.": 9,
    "Flush.": 6,
    "Straight.": 4,
    "Three of a kind.": 3,
    "Two pair.": 2,
    "Jacks or better.": 1,
    "Nothing.": 0,
}
pay_tables = {
    "Jacks or Better": {
        "name": "Jacks or Better",
        "Royal flush.": 800,
        "Straight flush.": 50,
        "Four of a kind.": 25,
        "Full house.": 9,
        "Flush.": 6,
        "Straight.": 4,
        "Three of a kind.": 3,
        "Two pair.": 2,
        "Jacks or better.": 1,
        "Nothing.": 0,
    },
    "Bonus Poker": {
        "name": "Bonus Poker",
        "Royal flush.": 800,
        "Straight flush.": 50,
        "Four aces.": 80,
        "Four 2-4.": 40,
        "Four 5-K.": 25,
        "Full house.": 8,
        "Flush.": 5,
        "Straight.": 4,
        "Three of a kind.": 3,
        "Two pair.": 2,
        "Jacks or better.": 1,
        "Nothing.": 0,
    },
}


def payout(hand, credit, bet_credits, user, pay_table="Bonus Poker"):
    table = pay_tables[pay_table]
    if pay_table == "Jacks or Better":
        table["Four aces."], table["Four 2-4."], table["Four 5-K."] = [
            table["Four of a kind."]
        ] * 3
    try:
        payout = table[evaluate_hand(hand)] * credit * bet_credits
    except KeyError:
        return 0
    if not user:
        return payout
    user.balance += payout
    if payout > 0:
        user.wins += 1
    else:
        user.losses += 1
    db.session.add(user)
    db.session.commit()
    return payout


def evaluate_hand(hand, pay_table="Bonus Poker"):
    cards = globals()["cards"]
    counter = Counter()
    info = [cards[card] for card in hand]
    [counter.update([card.face]) for card in info]
    suit = [card.suit for card in info]
    if 3 in counter.values():
        if 2 in counter.values():
            return "Full house."
        else:
            return "Three of a kind."
    if sorted(list(counter.values()), reverse=True)[:2] == [2, 2]:
        return "Two pair."
    elif 2 in [counter["Jack"], counter["Queen"], counter["King"], counter["Ace"]]:
        return "Jacks or better."
    if pay_table == "Bonus Poker" and counter["Ace"] == 4:
        return "Four aces."
    elif pay_table == "Bonus Poker" and 4 in [counter["2"], counter["3"], counter["4"]]:
        return "Four 2-4."
    elif pay_table == "Bonus Poker" and 4 in counter.values():
        return "Four 5-K."
    elif 4 in counter.values():
        return "Four of a kind."
    straights = [
        ["Ace", "2", "3", "4", "5"],
        ["2", "3", "4", "5", "6"],
        ["3", "4", "5", "6", "7"],
        ["4", "5", "6", "7", "8"],
        ["5", "6", "7", "8", "9"],
        ["6", "7", "8", "9", "10"],
        ["7", "8", "9", "10", "Jack"],
        ["8", "9", "10", "Jack", "Queen"],
        ["9", "10", "Jack", "Queen", "King"],
        ["10", "Jack", "Queen", "King", "Ace"],
    ]
    if sorted([card.face for card in info]) in [
        sorted(straight) for straight in straights
    ]:
        if suit[1:] == [suit[0]] * 4:
            if sorted([card.face for card in info]) == sorted(straights[-1]):
                return "Royal flush."
            else:
                return "Straight flush."
        else:
            return "Straight."
    if suit[1:] == [suit[0]] * 4:
        return "Flush."
    return "Nothing."


def draw_hand():
    cards = globals()["cards"]
    deck = list(cards.keys())
    random.shuffle(deck)
    hand = deck[:5]
    replacements = deck[5:10]
    return hand, replacements


def deal_replacements(hand, holds, replacements):
    new_hand = hand.copy()
    to_replace = replacements.copy()
    for index, card in enumerate(new_hand):
        if card not in holds:
            new_hand.remove(card)
            dealt = to_replace.pop(0)
            new_hand.insert(index, dealt)
    return new_hand


def main():
    cards = globals()["cards"]
    bank_roll = float(input("Bank roll: "))
    credit = 1
    bet_credits = 5
    points = 0
    while True:
        hand, replacements = draw_hand()
        bank_roll -= credit * bet_credits
        points += (credit * bet_credits) / 10
        info = [cards[card] for card in hand]
        winner = evaluate_hand(hand)
        print(", ".join([card.string for card in info]))
        if winner:
            print(winner)
        actions = list(input("Action: "))
        if actions == []:
            actions.append("d")
        action = actions.pop(0)
        if action == "h":
            holds = [hand[int(h) - 1] for h in actions]
            hold_info = [cards[card] for card in holds]
            print("Held: " + ", ".join([card.string for card in hold_info]))
            hand = deal_replacements(hand, holds, replacements)
            winner = evaluate_hand(hand)
            info = [cards[card] for card in hand]
            print(", ".join([card.string for card in info]))
            if winner:
                print(winner)
            bank_roll += payout(hand, credit, bet_credits)
            print(f"${bank_roll:,.2f}")
            time.sleep(4)
        elif action in list("12345"):
            actions = ["h", action] + actions
        elif action == "q":
            print(f"Session points: {points:,.0f}")
            break


if __name__ == "__main__":
    main()
