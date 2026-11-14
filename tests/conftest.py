import pytest

from app import app


@pytest.fixture(autouse=True)
def disable_login_for_existing_tests():
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test-secret"
    app.config["LOGIN_DISABLED"] = True
    yield
    app.config["LOGIN_DISABLED"] = False
