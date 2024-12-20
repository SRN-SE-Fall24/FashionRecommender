import pytest
from website import preferences


def login_user(client):
    mimetype = "application/x-www-form-urlencoded"
    headers = {"Content-Type": mimetype, "Accept": mimetype}

    # This user is not present in the db
    data = {"email": "test@gmail.com", "password": "password123"}
    url = "/login"

    response = client.post(url, data=data, headers=headers)
    if response.status_code == 200:
        return True
    return False


def test_get_default_preferences(app):
    client = app.test_client()
    if not login_user(client):
        assert False
    result = client.get("/default-preferences")
    assert result.json

