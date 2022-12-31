from app.poker import deal_replacements, draw_hand, evaluate_hand, pay_tables, payout


def test_draw_hand():
    """Draw 1,000 hands, assure that they are all valid, and never contain a duplicate card."""
    for count in range(1000):
        hand, replacements = draw_hand()
        assert len(set(hand + replacements)) == 10


def test_deal_replacements_0(sample_draw):
    """Deal replacements with 0 cards."""
    hand, replacements = sample_draw
    replaced = deal_replacements(hand, hand, replacements)
    assert hand == replaced


def test_deal_replacements_1(sample_draw):
    """Deal replacements holding 1 card."""
    hand, replacements = sample_draw
    holds = [hand[0]]
    replaced = deal_replacements(hand, holds, replacements)
    assert replaced == holds + replacements[0:4]


def test_deal_replacements_2(sample_draw):
    """Deal replacements holding 2 cards."""
    hand, replacements = sample_draw
    holds = [hand[0], hand[4]]
    replaced = deal_replacements(hand, holds, replacements)
    assert replaced == [hand[0]] + replacements[0:3] + [hand[4]]


def test_deal_replacements_3(sample_draw):
    """Deal replacements holding 3 cards."""
    hand, replacements = sample_draw
    holds = [hand[0], hand[2], hand[4]]
    replaced = deal_replacements(hand, holds, replacements)
    assert replaced == [hand[0], replacements[0], hand[2], replacements[1], hand[4]]


def test_deal_replacements_4(sample_draw):
    """Deal replacements holding 4 cards."""
    hand, replacements = sample_draw
    holds = [hand[0], hand[2], hand[3], hand[4]]
    replaced = deal_replacements(hand, holds, replacements)
    assert replaced == [hand[0], replacements[0], hand[2], hand[3], hand[4]]


def test_deal_replacements_5(sample_draw):
    """Deal replacements holding all 5 cards."""
    hand, replacements = sample_draw
    holds = []
    replaced = deal_replacements(hand, holds, replacements)
    assert not set(hand).intersection(set(replaced))


def test_evaluate_hand(winning_hands):
    """Test evaluation of the value of hands."""
    for table in pay_tables:
        for value, hand in winning_hands.items():
            if value not in pay_tables[table]:
                continue
            assert value == evaluate_hand(hand, pay_tables[table]["name"])


def test_payout(winning_hands, sample_user):
    """Test the payouts for possible hands."""
    for name, table in pay_tables.items():
        for value, credits in table.copy().items():
            if value == "name":
                continue
            assert credits == payout(winning_hands[value], 1, 1, sample_user, name)
