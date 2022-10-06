from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home():
    response = client.get(
        "/", headers={"content-type": "text/html; charset=utf-8"})
    assert response.status_code == 200
    assert b"Welcome to FarMLife. Computer Vision made easy for AgTech" in response.content
    response = client.get("/static/css/style3.css")
    assert response.status_code == 200


def test_page_about():
    response = client.get("/page/about",
                          headers={"content-type": "text/html; charset=utf-8"})
    assert response.status_code == 200
    assert b"About" in response.content


def test_label():
    response = client.get("/label",
                          headers={"content-type": "text/html; charset=utf-8"})

    assert response.status_code == 200
    assert b"Label Finder" in response.content


def test_analytics():
    response = client.get("/analytics",
                          headers={"content-type": "text/html; charset=utf-8"})
    assert response.status_code == 200
    assert b"Analytics" in response.content


def test_upload():
    response = client.post("/upload", data={"tag": "flower"}, headers={
                           "Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 200
    assert b"Upload" in response.content


