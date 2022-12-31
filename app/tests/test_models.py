from app.models import User, Hand


def test_user_repr(sample_user):
    assert "<User sample_user>" == repr(sample_user)


def test_user_set_password(sample_user):
    sample_password = "Sample123!"
    sample_user.set_password(sample_password)
    assert sample_user.check_password(sample_password)
    assert sample_user.password_hash != sample_password


def test_user_get_reset_password_token(app, sample_user):
    with app.app_context():
        print(sample_user)
        token = sample_user.get_reset_password_token()
        assert User.verify_reset_password_token(token) == sample_user


def test_hand_repr(sample_hand):
    assert "<Hand ['TS', 'JS', 'QS', 'KS', 'AS']>" == repr(sample_hand)


def test_hand_str(sample_hand):
    correct = (
        "10 of Spades, Jack of Spades, Queen of Spades, King of Spades, Ace of Spades"
    )
    assert correct == str(sample_hand)


def test_hand_evaluate(sample_hand):
    correct = "Royal flush."
    assert correct == sample_hand.evaluate()
