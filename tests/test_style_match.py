import pytest
import json


def test_style_match_status(app):
    client = app.test_client()
    with client.session_transaction() as sess:
        sess["userid"] = 1
    headers = {
        "Content-Type": "multipart/form-data"
    }
    with open('tests/sample_data/sample_shirt.jpg', "rb") as img_file:
        data={'clothingImage': (img_file, "test_image.jpg")}
        response = client.post("/style_match", data=data, headers=headers)
    assert response.status_code == 200

    
def test_style_match_outfits(app):
    client = app.test_client()
    with client.session_transaction() as sess:
        sess["userid"] = 1
    headers = {
        "Content-Type": "multipart/form-data"
    }
    with open('tests/sample_data/sample_shirt.jpg', "rb") as img_file:
        data={'clothingImage': (img_file, "test_image.jpg")}
        response = client.post("/style_match", data=data, headers=headers)
    
    res = eval(response.json['recommendations'][7:-4])
    assert 'recommended_outfits' in res
    outfits = res['recommended_outfits']
    assert len(outfits) > 0
    for i in outfits:
        assert 'name' in i
        assert 'description' in i


def test_style_match_tips(app):
    client = app.test_client()
    with client.session_transaction() as sess:
        sess["userid"] = 1
    headers = {
        "Content-Type": "multipart/form-data"
    }
    with open('tests/sample_data/sample_shirt.jpg', "rb") as img_file:
        data={'clothingImage': (img_file, "test_image.jpg")}
        response = client.post("/style_match", data=data, headers=headers)
    
    res = eval(response.json['recommendations'][7:-4])
    assert 'style_tips' in res
    tips = res['style_tips']
    assert len(tips) > 0
    for i in tips:
        assert isinstance(i, str)
