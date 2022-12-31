from datetime import datetime

import pytest

from app import create_app, db
from app.models import User, Hand


@pytest.fixture(scope="module")
def sample_draw():
    return [["TS", "JS", "QS", "KS", "AS"], ["TH", "JH", "QH", "KH", "AH"]]


@pytest.fixture
def winning_hands():
    return {
        "Royal flush.": ["TS", "JS", "QS", "KS", "AS"],
        "Four aces.": ["AC", "AD", "AH", "AS", "TS"],
        "Straight flush.": ["9S", "TS", "JS", "QS", "KS"],
        "Four 2-4.": ["2C", "2D", "2S", "2H", "7H"],
        "Four 5-K.": ["5C", "5D", "5H", "5S", "6H"],
        "Four of a kind.": ["7C", "7D", "7H", "7S", "2D"],
        "Full house.": ["AC", "AD", "AH", "4S", "4C"],
        "Flush.": ["JS", "5S", "8S", "KS", "6S"],
        "Straight.": ["TH", "JD", "QC", "KS", "AS"],
        "Three of a kind.": ["2S", "2H", "2D", "3S", "4H"],
        "Two pair.": ["7S", "7H", "6H", "6D", "2C"],
        "Jacks or better.": ["AC", "AH", "4C", "2D", "TS"],
        "Nothing.": ["AS", "2S", "3S", "4S", "4C"],
    }


@pytest.fixture(scope="module")
def sample_hand(sample_user, sample_draw):
    return Hand(id=1, dealt=sample_draw[0], hand=sample_draw[0], user_id=sample_user.id)


@pytest.fixture(scope="module")
def app():
    app = create_app()
    app.config.update(
        {
            "SQLALCHEMY_DATABASE_URI": "sqlite:///",
            "SECRET_KEY": "testing",
            "TESTING": True,
        }
    )
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture(scope="module")
def sample_user(app):
    user = User(
        id=1000,
        username="sample_user",
        email="sample@user.test",
        joined=datetime(2022, 1, 1),
        wins=10,
        losses=10,
        points=1000,
        bet=1,
        balance=100,
    )
    with app.app_context():
        db.session.add(user)
        db.session.commit()
        yield user
