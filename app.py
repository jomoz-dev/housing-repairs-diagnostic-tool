from datetime import datetime

import sqlite3

import csv

from flask import Flask, render_template, request  # type: ignore[reportMissingImports]
from flask import send_file

from diagnosis import diagnose_repair


app = Flask(__name__)

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
        assessment_date=assessment_date
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

    if priority and repair_type:

        cursor.execute(
            """
            SELECT *
            FROM assessments
            WHERE priority = ?
            AND repair_type = ?
            ORDER BY id DESC
            """,
            (priority, repair_type)
        )

    elif priority:

        cursor.execute(
            """
            SELECT *
            FROM assessments
            WHERE priority = ?
            ORDER BY id DESC
            """,
            (priority,)
        )

    elif repair_type:

        cursor.execute(
            """
            SELECT *
            FROM assessments
            WHERE repair_type = ?
            ORDER BY id DESC
            """,
            (repair_type,)
        )

    else:

        cursor.execute(
            """
            SELECT *
            FROM assessments
            ORDER BY id DESC
            """
        )
    records = cursor.fetchall()

    connection.close()

    return render_template(
        "history.html",
        records=records
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



if __name__ == "__main__":
    app.run(debug=True)
