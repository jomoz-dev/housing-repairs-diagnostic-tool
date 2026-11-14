from app import app


def test_unauthenticated_request_redirects_to_login():
    app.config["LOGIN_DISABLED"] = False
    client = app.test_client()
    response = client.get("/history", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_wrong_password_does_not_sign_in():
    app.config["LOGIN_DISABLED"] = False
    client = app.test_client()
    response = client.post(
        "/login",
        data={"username": "advisor", "password": "wrong"},
        follow_redirects=False,
    )
    assert response.status_code == 200
    assert b"not correct" in response.data
    blocked = client.get("/history", follow_redirects=False)
    assert blocked.status_code == 302


def test_valid_login_can_open_history():
    app.config["LOGIN_DISABLED"] = False
    client = app.test_client()
    response = client.post(
        "/login",
        data={"username": "advisor", "password": "changeme"},
        follow_redirects=False,
    )
    assert response.status_code == 302
    history = client.get("/history", follow_redirects=False)
    assert history.status_code == 200


def test_logout_clears_session():
    app.config["LOGIN_DISABLED"] = False
    client = app.test_client()
    client.post(
        "/login",
        data={"username": "advisor", "password": "changeme"},
    )
    client.get("/logout")
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]
