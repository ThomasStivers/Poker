import collections
import itertools
import random
import time


Card = collections.namedtuple("card", ["face", "suit"])
faces = "2 3 4 5 6 7 8 9 10 Jack Queen King Ace".split(" ")
suits = "Clubs Diamonds Hearts Spades".split(" ")
cards = [Card(c[0], c[1]) for c in itertools.product(faces, suits)]
keys = [''.join(card) for card in list(itertools.product([f[0] if f != "10" else "T"for f in faces], [s[0] for s in suits]))]
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
    None: 0,
}

def payout(hand, credit=0.25, bet_credits=5):
    try:
        return pay_table[evaluate(hand)] * credit * bet_credits
    except KeyError:
        return 0

def evaluate(hand):
    counter = collections.Counter()
    [counter.update([card.split(" of ")[0]]) for card in hand]
    if 3 in counter.values():
        if 2 in counter.values():
            return "Full house."
        else:
            return "Three of a kind."
    if sorted(list(counter.values()), reverse=True)[:2] == [2, 2]:
        return "Two pair."
    elif 2 in [counter["Jack"], counter["Queen"], counter["King"], counter["Ace"]]:
        return "Jacks or better."
    if 4 in counter.values():
        return "Four of a kind."
    straights = [["Ace", "2", "3", "4", "5"], ["2", "3", "4", "5", "6"], ["3", "4", "5", "6", "7"], ["4", "5", "6", "7", "8"], ["5", "6", "7", "8", "9"], ["6", "7", "8", "9", "10"], ["7", "8", "9", "10", "Jack"], ["8", "9", "10", "Jack", "Queen"], ["9", "10", "Jack", "Queen", "King"], ["10", "Jack", "Queen", "King", "Ace"]]
    if sorted([card.split(" of")[0] for card in hand]) in [sorted(straight) for straight in straights]:
        suit = [card.split(" of ")[1] for card in hand]
        if suit[1:] == [suit[0]] * 4:
            if sorted([card.split(" of ")[0] for card in hand]) == straights[-1]:
                return "Royal flush."
            else:
                return "Straight flush."
        else:
            return "Straight."
    suit = [card.split(" of ")[1] for card in hand]
    if suit[1:] == [suit[0]] * 4:
        return "Flush."


def main():
    f = [f[0] for f in faces]
    f[8] = "T"
    s = [s[0] for s in suits]
    bank_roll = float(input("Bank roll: "))
    credit = 1
    bet_credits = 5
    points = 0
    while True:
        cards = list(itertools.product(faces, suits))
        long = [' of '.join(item) for item in cards]
        random.shuffle(cards)
        bank_roll -= credit * bet_credits
        points += (credit * bet_credits) / 10
        hand=cards[:5]
        cards = cards[6:]
        hand = [" of ".join(c) for c in hand]
        print(", ".join(hand))
        if evaluate(hand):
            print(evaluate(hand))
        actions = list(input("Action: "))
        if actions == []: actions.append("d")
        action = actions.pop(0)
        if action == "h":
            holds = [hand[int(h) - 1] for h in actions]
            print(f" Held: {holds}")
            for index, card in enumerate(hand):
                if card not in holds:
                    hand.remove(card)
                    dealt = " of ".join(cards.pop(0))
                    hand.insert(index, dealt)
            print(", ".join(hand))
            if evaluate(hand): print(evaluate(hand))
            # if payout(hand): print(payout(hand))
            bank_roll += payout(hand, credit, bet_credits)
            print(f"${bank_roll:,.2f}")
            time.sleep(4)
        elif action in list("12345"): actions = ["h", action] + actions
        elif action == "q":
            print(f"Session points: {points:,.0f}")
            break

def draw_hand():
    cards = globals()["cards"]
    deck = list(cards.keys())
    random.shuffle(deck)
    hand = deck[:5]
    deck = deck[6:]
    return [cards[card] for card in hand]

def hold_cards(hand):
    pass

if __name__ == "__main__":
    print(draw_hand())
