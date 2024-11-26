import pytest
import json


def test_color_palettes_status(app):
    client = app.test_client()
    with client.session_transaction() as sess:
        sess["userid"] = 1
    data = json.dumps({"occasion": "Dandiya", "culture": "Indian", "gender": "female", "ageGroup": "Adults"})
    headers = {
        "Content-Type": "application/json"
    }
    response = client.post("/recommendations", data=data, headers=headers)
    assert response.status_code == 200


def test_color_palettes_count(app):
    client = app.test_client()
    with client.session_transaction() as sess:
        sess["userid"] = 1
    data = json.dumps({"occasion": "Marriage", "culture": "Indian", "gender": "male", "ageGroup": "Adults"})
    headers = {
        "Content-Type": "application/json"
    }
    response = client.post("/recommendations", data=data, headers=headers)
    assert 'COLOR_PALETTES' in response.json
    color_palettes = eval(response.json['COLOR_PALETTES'][7:-4])
    assert len(color_palettes) == 3

    
def test_color_palettes_structure(app):
    client = app.test_client()
    with client.session_transaction() as sess:
        sess["userid"] = 1
    data = json.dumps({"occasion": "Party", "culture": "American", "gender": "female", "ageGroup": "Teenagers"})
    headers = {
        "Content-Type": "application/json"
    }
    response = client.post("/recommendations", data=data, headers=headers)
    assert 'COLOR_PALETTES' in response.json
    assert isinstance(response.json['COLOR_PALETTES'], str)
    color_palettes = eval(response.json['COLOR_PALETTES'][7:-4])
    for palette in color_palettes:
        assert len(palette) == 5
        for color_item in palette:
            assert len(color_item) == 2
            assert isinstance(color_item[0], str)
            assert isinstance(color_item[1], str)

