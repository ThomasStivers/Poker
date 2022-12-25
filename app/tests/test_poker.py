from app.poker import deal_replacements, draw_hand


def test_draw_hand():
    """Draw 100,000 hands, assure that they are all valid, and never contain a duplicate card."""
    for count in range(100000):
        hand, replacements = draw_hand()
        assert len(set(hand + replacements)) == 10


def test_deal_replacements_0():
    """Deal replacements with 0 cards."""
    hand, replacements = draw_hand()
    replaced = deal_replacements(hand, hand, replacements)
    assert hand == replaced


def test_deal_replacements_1():
    """Deal replacements holding 1 card."""
    hand, replacements = draw_hand()
    holds = [hand[0]]
    replaced = deal_replacements(hand, holds, replacements)
    assert replaced == holds + replacements[0:4]


def test_deal_replacements_2():
    """Deal replacements holding 2 cards."""
    hand, replacements = draw_hand()
    holds = [hand[0], hand[4]]
    replaced = deal_replacements(hand, holds, replacements)
    assert replaced == [hand[0]] + replacements[0:3] + [hand[4]]


def test_deal_replacements_3():
    """Deal replacements holding 3 cards."""
    hand, replacements = draw_hand()
    holds = [hand[0], hand[2], hand[4]]
    replaced = deal_replacements(hand, holds, replacements)
    assert replaced == [hand[0], replacements[0], hand[2], replacements[1], hand[4]]


def test_deal_replacements_4():
    """Deal replacements holding 4 cards."""
    hand, replacements = draw_hand()
    holds = [hand[0], hand[2], hand[3], hand[4]]
    replaced = deal_replacements(hand, holds, replacements)
    assert replaced == [hand[0], replacements[0], hand[2], hand[3], hand[4]]


def test_deal_replacements_5():
    """Deal replacements holding all 5 cards."""
    hand, replacements = draw_hand()
    holds = []
    replaced = deal_replacements(hand, holds, replacements)
    assert not set(hand).intersection(set(replaced))
