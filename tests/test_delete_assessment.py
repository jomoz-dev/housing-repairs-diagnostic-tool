import sqlite3

from app import app
from tests.test_edit_notes import _prepare_db


def test_get_delete_page_does_not_remove_record(tmp_path, monkeypatch):
    db_path = tmp_path / "repairs.db"
    _prepare_db(db_path)
    real_connect = sqlite3.connect

    def connect(_path="repairs.db", **kwargs):
        return real_connect(db_path, **kwargs)

    monkeypatch.setattr("app.sqlite3.connect", connect)

    client = app.test_client()
    response = client.get("/assessment/1/delete")
    assert response.status_code == 200
    assert b"HR-20261114-010000" in response.data

    connection = real_connect(db_path)
    count = connection.execute(
        "SELECT COUNT(*) FROM assessments"
    ).fetchone()[0]
    connection.close()
    assert count == 1


def test_confirmed_delete_removes_record(tmp_path, monkeypatch):
    db_path = tmp_path / "repairs.db"
    _prepare_db(db_path)
    real_connect = sqlite3.connect

    def connect(_path="repairs.db", **kwargs):
        return real_connect(db_path, **kwargs)

    monkeypatch.setattr("app.sqlite3.connect", connect)

    client = app.test_client()
    response = client.post(
        "/assessment/1/delete",
        data={"confirm": "yes"},
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert "/history" in response.headers["Location"]

    connection = real_connect(db_path)
    count = connection.execute(
        "SELECT COUNT(*) FROM assessments"
    ).fetchone()[0]
    connection.close()
    assert count == 0


def test_delete_without_confirm_keeps_record(tmp_path, monkeypatch):
    db_path = tmp_path / "repairs.db"
    _prepare_db(db_path)
    real_connect = sqlite3.connect

    def connect(_path="repairs.db", **kwargs):
        return real_connect(db_path, **kwargs)

    monkeypatch.setattr("app.sqlite3.connect", connect)

    client = app.test_client()
    response = client.post(
        "/assessment/1/delete",
        data={},
        follow_redirects=False,
    )
    assert response.status_code == 302

    connection = real_connect(db_path)
    count = connection.execute(
        "SELECT COUNT(*) FROM assessments"
    ).fetchone()[0]
    connection.close()
    assert count == 1


def test_delete_unknown_record_is_not_found(tmp_path, monkeypatch):
    db_path = tmp_path / "repairs.db"
    _prepare_db(db_path)
    real_connect = sqlite3.connect

    def connect(_path="repairs.db", **kwargs):
        return real_connect(db_path, **kwargs)

    monkeypatch.setattr("app.sqlite3.connect", connect)

    client = app.test_client()
    response = client.get("/assessment/99/delete")
    assert response.status_code == 404
