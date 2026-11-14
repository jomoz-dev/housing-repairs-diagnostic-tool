import sqlite3

from app import app


SCHEMA = """
CREATE TABLE assessments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reference TEXT,
    repair_type TEXT,
    priority TEXT,
    trade TEXT,
    attendance TEXT,
    message TEXT,
    assessment_date TEXT
)
"""


def _prepare_db(path):
    connection = sqlite3.connect(path)
    connection.execute(SCHEMA)
    connection.execute(
        """
        INSERT INTO assessments (
            reference,
            repair_type,
            priority,
            trade,
            attendance,
            message,
            assessment_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "HR-20261114-010000",
            "electrical",
            "Urgent",
            "Electrician",
            "24 Hours",
            "Complete loss of power reported.",
            "14/11/2026 01:00",
        ),
    )
    connection.commit()
    connection.close()


def test_edit_notes_updates_message_only(tmp_path, monkeypatch):
    db_path = tmp_path / "repairs.db"
    _prepare_db(db_path)

    real_connect = sqlite3.connect

    def connect(_path="repairs.db", **kwargs):
        return real_connect(db_path, **kwargs)

    monkeypatch.setattr("app.sqlite3.connect", connect)

    client = app.test_client()
    response = client.post(
        "/assessment/1/notes",
        data={"message": "  Power restored at meter. Follow-up still needed.  "},
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert "/history" in response.headers["Location"]

    connection = sqlite3.connect(db_path)
    row = connection.execute(
        "SELECT message, priority, trade FROM assessments WHERE id = 1"
    ).fetchone()
    connection.close()

    assert row[0] == "Power restored at meter. Follow-up still needed."
    assert row[1] == "Urgent"
    assert row[2] == "Electrician"


def test_edit_notes_unknown_record_is_not_found(tmp_path, monkeypatch):
    db_path = tmp_path / "repairs.db"
    _prepare_db(db_path)

    real_connect = sqlite3.connect

    def connect(_path="repairs.db", **kwargs):
        return real_connect(db_path, **kwargs)

    monkeypatch.setattr("app.sqlite3.connect", connect)

    client = app.test_client()
    response = client.get("/assessment/99/notes")
    assert response.status_code == 404
