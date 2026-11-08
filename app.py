from datetime import datetime

import sqlite3

from flask import Flask, render_template, request

app = Flask(__name__)

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

@app.route("/diagnose", methods=["POST"])
def diagnose():
    
    danger = request.form.get("danger", "no")
    unsafe_property = request.form.get("unsafe_property", "no")
    vulnerable = request.form.get("vulnerable", "no")

    #Water Leak Decision Tree
    active_leak = request.form.get("active_leak", "no")
    contained = request.form.get("contained", "yes")
    electrics_affected = request.form.get("electrics_affected", "no")
    repair_type = request.form["repair_type"]

    #Electrical Decision Tree
    sparking = request.form.get("sparking", "no") 
    burning_smell = request.form.get("burning_smell", "no") 
    power_loss = request.form.get("power_loss", "no")

    #Heating Decision Tree
    heating_failed = request.form.get("heating_failed", "no")
    hot_water = request.form.get("hot_water", "no")
    
    #Damp & Mould Decision Tree
    visible_mould = request.form.get(
    "visible_mould",
    "no"
    )

    long_term_issue = request.form.get(
        "long_term_issue",
        "no"
    )

    children_present = request.form.get(
        "children_present",
        "no"
    )

    respiratory_condition = request.form.get(
        "respiratory_condition",
        "no"
    )

    # Emergency safety assessment

    if danger == "yes" or unsafe_property == "yes":

        result = {
            "repair_type": repair_type,
            "priority": "Emergency",
            "trade": "Emergency Contractor",
            "attendance": "Within 24 Hours",
            "message": "Potential health and safety risk identified."
        }

    # Water Leak Decision Tree

    elif repair_type == "water_leak":

        if electrics_affected == "yes":

            result = {
                "priority": "Emergency",
                "repair_type": repair_type,
                "trade": "Plumber / Electrician",
                "attendance": "2-4  Hours",
                "message": "Water is affecting electrical fittings."
            }

        elif active_leak == "yes" and contained == "no":

            result = {
                
                "repair_type": repair_type,
                "priority": "Emergency",
                "trade": "Plumber",
                "attendance": "24 Hours",
                "message": "Active leak cannot be contained."
            }

        elif active_leak == "yes":

            result = {
                "repair_type": repair_type,
                "priority": "Urgent",
                "trade": "Plumber",
                "attendance": "72 Hours",
                "message": "Active leak reported."
            }

        else:

            result = {
                "repair_type": repair_type,
                "priority": "Routine",
                "trade": "Plumber",
                "attendance": "28 Days",
                "message": "Leak investigation required."
            }

    # Electrical

    elif repair_type == "electrical":

        if sparking == "yes" or burning_smell == "yes":

            result = {
                "repair_type": repair_type,
                "priority": "Emergency",
                "trade": "Electrician",
                "attendance": "2-4 Hours",
                "message": "Potential electrical safety risk identified."
            }

        elif power_loss == "yes":

            result = {
                "repair_type": repair_type,
                "priority": "Urgent",
                "trade": "Electrician",
                "attendance": "24 Hours",
                "message": "Complete loss of power reported."
            }

        else:

            result = {
                "repair_type": repair_type,
                "priority": "Routine",
                "trade": "Electrician",
                "attendance": "28 Days",
                "message": "Electrical inspection required."
            }
    # Heating

    elif repair_type == "heating":

        if heating_failed == "yes" and vulnerable == "yes":

            result = {
                "repair_type": repair_type,
                "priority": "Emergency",
                "trade": "Heating Engineer",
                "attendance": "4 Hours",
                "message": "Vulnerable resident without heating."
            }

        elif heating_failed == "yes":

            result = {
                "repair_type": repair_type,
                "priority": "Urgent",
                "trade": "Heating Engineer",
                "attendance": "24 Hours",
                "message": "Heating failure reported."
            }

        elif hot_water == "yes":

            result = {
                "repair_type": repair_type,
                "priority": "Urgent",
                "trade": "Heating Engineer",
                "attendance": "24 Hours",
                "message": "Loss of hot water reported."
            }

        else:

            result = {
                "repair_type": repair_type,
                "priority": "Routine",
                "trade": "Heating Engineer",
                "attendance": "28 Days",
                "message": "Heating inspection required."
            }
    
    # Damp & Mould

    elif repair_type == "damp_mould":

        if (
            visible_mould == "yes"
            and respiratory_condition == "yes"
        ):

            result = {
                "repair_type": repair_type,
                "priority": "Urgent",
                "trade": "Damp Specialist",
                "attendance": "7 Days",
                "message": "Visible mould and respiratory risk identified."
            }

        elif (
            visible_mould == "yes"
            and children_present == "yes"
        ):

            result = {
                "repair_type": repair_type,
                "priority": "Urgent",
                "trade": "Damp Specialist",
                "attendance": "7 Days",
                "message": "Visible mould affecting vulnerable occupants."
            }

        elif (
            visible_mould == "yes"
            and long_term_issue == "yes"
        ):

            result = {
                "repair_type": repair_type,
                "priority": "Urgent",
                "trade": "Damp Specialist",
                "attendance": "7 Days",
                "message": "Long-term damp and mould issue reported."
            }

        else:

            result = {
                "repair_type": repair_type,
                "priority": "Routine",
                "trade": "Damp Specialist",
                "attendance": "28 Days",
                "message": "Damp inspection required."
            }


    # Roofing
    elif repair_type == "roof leak":

    
            if electrics_affected == "yes":
    
                result = {
                    "repair_type": repair_type,
                    "priority": "Emergency",
                    "trade": "Electrician",
                    "attendance": "2-4  Hours",
                    "message": "Water is affecting electrics."
                }
    
    else:

        result = {
            "repair_type": repair_type,
            "priority": "Routine",
            "trade": "Roofer",
            "attendance": "28 Days",
            "message": "Roofing issue reported."
        }

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
            message
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            reference,
            result["repair_type"],
            result["priority"],
            result["trade"],
            result["attendance"],
            result["message"]
        )
    )

    connection.commit()

    connection.close()

    display_names = {
    "water_leak": "Water Leak",
    "electrical": "Electrical",
    "heating": "Heating"
    }

    result["repair_type"] = display_names.get(
        repair_type,
        repair_type
    )

    return render_template(
        "result.html",
        result=result,
        reference=reference,
        assessment_date=assessment_date
    )

@app.route("/dashboard")
def dashboard():

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

    connection.close()

    return render_template(
        "dashboard.html",
        total=total,
        emergency=emergency,
        urgent=urgent,
        routine=routine
    )

@app.route("/history")
def history():

    connection = sqlite3.connect(
        "repairs.db"
    )

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

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

if __name__ == "__main__":
    app.run(debug=True)