import pytest


def login(client):
    return client.post(
        "/auth/signin", data={"username": "sample_user", "password": "SamplePassword"}
    )


def test_index(client):
    """
    GIVEN: a running flask app
    WHEN: a GET request for the / endpoint
    THEN: verify status code for okay and text from the templates/index.html
    """
    response = client.get("/")
    assert response.status_code == 200
    assert b"Accessible Video Poker" in response.data
    assert b"get registered" in response.data


def test_index_post(client):
    """
    GIVEN: a running flask app
    WHEN: a post request is made to the / endpoint
    THEN: set status code to bad request and do not return the endpoint
    """
    response = client.post("/")
    assert response.status_code == 405
    assert b"Accessible Video Poker" not in response.data


def test_login_required(client):
    """
    GIVEN: no logged in user
    WHEN: connecting to endpoints where login is required
    THEN: redirect to the /auth/signin endpoint
    """
    login_required_endpoints = ["/atm", "/bet", "/play"]
    redirect_status_code = 302
    signin_page = b"/auth/signin"
    responses = [client.get(endpoint) for endpoint in login_required_endpoints]
    for response in responses:
        assert response.status_code == redirect_status_code
        assert signin_page in response.data


@pytest.mark.usefixtures("logged_in")
def test_bet(client):
    """
    GIVEN: a logged in user
    WHEN: the /bet endpoint is accessed with a GET request
    THEN: the bet template is returned
    """
    response = client.get("/bet")
    assert b"redirect" not in response.data
    assert response.status_code != 302
