from datetime import datetime

import sqlite3

import csv

from flask import Flask, render_template, request  # type: ignore[reportMissingImports]
from flask import abort, redirect, send_file, url_for

from diagnosis import diagnose_repair


app = Flask(__name__)


def parse_stored_date(value):
    if not value:
        return None
    for fmt in ("%d/%m/%Y %H:%M", "%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    return None


def parse_query_date(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def record_in_date_range(assessment_date, date_from, date_to):
    if not date_from and not date_to:
        return True
    stored = parse_stored_date(assessment_date)
    if stored is None:
        return False
    stored_day = stored.date()
    if date_from and stored_day < date_from:
        return False
    if date_to and stored_day > date_to:
        return False
    return True

#Homepage Route
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/assessment", methods=["POST"])
def assessment():

    repair_type = request.form["repair_type"]

    if repair_type == "water_leak":

        return render_template("water_leak.html")

    elif repair_type == "electrical":

        return render_template("electrical.html")

    elif repair_type == "heating":

        return render_template("heating.html")

    elif repair_type == "damp_mould":

        return render_template(
            "damp_mould.html"
        )

    elif repair_type == "roofing":

        return render_template(
            "roofing.html"
        )

    elif repair_type == "doors_windows":

        return render_template(
            "doors_windows.html"
        )

#Diagnose Route    
@app.route("/diagnose", methods=["POST"])
def diagnose():

    result = diagnose_repair(request.form)

    reference = datetime.now().strftime(
    "HR-%Y%m%d-%H%M%S"
    )
    print(result)

    assessment_date = datetime.now().strftime(
        "%d/%m/%Y %H:%M"
    )

    connection = sqlite3.connect(
    "repairs.db"
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO assessments
        (
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
            reference,
            result["repair_type"],
            result["priority"],
            result["trade"],
            result["attendance"],
            result["message"],
            assessment_date
        )
    )

    assessment_id = cursor.lastrowid

    connection.commit()

    connection.close()

    display_names = {
        "water_leak": "Water Leak",
        "electrical": "Electrical",
        "heating": "Heating",
        "damp_mould": "Damp & Mould",
        "roofing": "Roofing",
        "doors_windows": "Doors & Windows"
    }

    result["repair_type"] = display_names.get(
        result["repair_type"],
        result["repair_type"]
    )

    return render_template(
        "result.html",
        result=result,
        reference=reference,
        assessment_date=assessment_date,
        assessment_id=assessment_id
    )

#Dashboard Route
@app.route("/dashboard")
def dashboard():

    display_names = {
                "water_leak": "Water Leak",
                "electrical": "Electrical",
                "heating": "Heating",
                "damp_mould": "Damp & Mould",
                "roofing": "Roofing",
                "doors_windows": "Doors & Windows"
            }
    
    
    connection = sqlite3.connect(
        "repairs.db"
    )

    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM assessments"
    )

    total = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM assessments
        WHERE priority='Emergency'
        """
    )

    emergency = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM assessments
        WHERE priority='Urgent'
        """
    )

    urgent = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM assessments
        WHERE priority='Routine'
        """
    )

    routine = cursor.fetchone()[0]

    emergency_percent = round(
        emergency / total * 100, 1
    ) if total else 0

    urgent_percent = round(
        urgent / total * 100, 1
    ) if total else 0

    routine_percent = round(
        routine / total * 100, 1
    ) if total else 0


    cursor.execute("""
        SELECT repair_type,
            COUNT(*) AS total
        FROM assessments
        GROUP BY repair_type
        ORDER BY total DESC
    """)

    repair_stats = cursor.fetchall()

    formatted_stats = []

    max_repair_count = 0

    for repair_type, total_count in repair_stats:

        if total_count > max_repair_count:
            max_repair_count = total_count

        formatted_stats.append(
            {
                "name": display_names.get(
                    repair_type,
                    repair_type
                ),
                "count": total_count,
                "percent": round(
                    total_count / total * 100, 1
                ) if total else 0,
                "width": round(
                    total_count / max_repair_count * 100, 1
                ) if max_repair_count else 0,
            }
        )

    # Widths depend on the largest group; recalculate now the max is known.
    for row in formatted_stats:
        row["width"] = round(
            row["count"] / max_repair_count * 100, 1
        ) if max_repair_count else 0

    connection.close()

    return render_template(
        "dashboard.html",
        total=total,
        emergency=emergency,
        urgent=urgent,
        routine=routine,
        repair_stats=formatted_stats,
        emergency_percent=emergency_percent,
        urgent_percent=urgent_percent,
        routine_percent=routine_percent,
    )

#Export Route
@app.route("/export")
def export():

    connection = sqlite3.connect(
        "repairs.db"
    )

    cursor = connection.cursor()

    priority = request.args.get(
        "priority",
        ""
    )

    if priority:

        cursor.execute(
            """
            SELECT *
            FROM assessments
            WHERE priority = ?
            """,
            (priority,)
        )

    else:

        cursor.execute(
            """
            SELECT *
            FROM assessments
            """
        )
    

    records = cursor.fetchall()

    connection.close()

    with open(
        "assessments.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "ID",
            "Reference",
            "Repair Type",
            "Priority",
            "Trade",
            "Attendance",
            "Notes",
            "Assessment Date"
        ])

        writer.writerows(records)

    return send_file(
        "assessments.csv",
        as_attachment=True
    )


#History Route
@app.route("/history")
def history():

    connection = sqlite3.connect(
        "repairs.db"
    )

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    priority = request.args.get(
        "priority",
        ""
    )

    repair_type = request.args.get(
        "repair_type",
        ""
    )

    date_from_text = request.args.get(
        "date_from",
        ""
    )

    date_to_text = request.args.get(
        "date_to",
        ""
    )

    date_from = parse_query_date(date_from_text)
    date_to = parse_query_date(date_to_text)

    clauses = []
    params = []

    if priority:
        clauses.append("priority = ?")
        params.append(priority)

    if repair_type:
        clauses.append("repair_type = ?")
        params.append(repair_type)

    query = "SELECT * FROM assessments"
    if clauses:
        query += " WHERE " + " AND ".join(clauses)
    query += " ORDER BY id DESC"

    cursor.execute(query, params)
    records = [
        row for row in cursor.fetchall()
        if record_in_date_range(
            row["assessment_date"],
            date_from,
            date_to
        )
    ]

    connection.close()

    return render_template(
        "history.html",
        records=records,
        selected_priority=priority,
        selected_repair_type=repair_type,
        date_from=date_from_text,
        date_to=date_to_text
    )

#Search route
@app.route("/search", methods=["GET", "POST"])
def search():

    if request.method == "POST":

        reference = request.form["reference"]

        conn = sqlite3.connect(
            "repairs.db"
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM assessments
            WHERE reference = ?
            """,
            (reference,)
        )

        result = cursor.fetchone()

        conn.close()

        return render_template(
            "search_result.html",
            result=result
        )

    return render_template(
        "search.html"
    )


def get_assessment(assessment_id):
    connection = sqlite3.connect(
        "repairs.db"
    )
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT *
        FROM assessments
        WHERE id = ?
        """,
        (assessment_id,)
    )
    record = cursor.fetchone()
    connection.close()
    return record


@app.route(
    "/assessment/<int:assessment_id>/notes",
    methods=["GET", "POST"]
)
def edit_notes(assessment_id):

    record = get_assessment(assessment_id)

    if record is None:
        abort(404)

    if request.method == "POST":
        notes = request.form.get("message", "").strip()

        connection = sqlite3.connect(
            "repairs.db"
        )
        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE assessments
            SET message = ?
            WHERE id = ?
            """,
            (notes, assessment_id)
        )
        connection.commit()
        connection.close()

        return redirect(url_for("history"))

    display_names = {
        "water_leak": "Water Leak",
        "electrical": "Electrical",
        "heating": "Heating",
        "damp_mould": "Damp & Mould",
        "roofing": "Roofing",
        "doors_windows": "Doors & Windows"
    }

    return render_template(
        "edit_notes.html",
        record=record,
        repair_type_label=display_names.get(
            record["repair_type"],
            record["repair_type"]
        )
    )


if __name__ == "__main__":
    app.run(debug=True)
