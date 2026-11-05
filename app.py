@app.route("/diagnose", methods=["POST"])
def diagnose():

    danger = request.form["danger"]
    unsafe_property = request.form["unsafe_property"]
    vulnerable = request.form["vulnerable"]

    repair_type = request.form["repair_type"]

    active_leak = request.form["active_leak"]

    if danger == "yes" or unsafe_property == "yes":

        result = {
            "priority": "Emergency",
            "trade": "Emergency Contractor",
            "attendance": "Within 24 Hours",
            "message": "Potential health and safety risk identified."
        }

    elif repair_type == "water_leak":

        if active_leak == "yes":

            result = {
                "priority": "Emergency",
                "trade": "Plumber",
                "attendance": "24 Hours",
                "message": "Active water escape reported."
            }

        else:

            result = {
                "priority": "Urgent",
                "trade": "Plumber",
                "attendance": "48 Hours",
                "message": "Water leak investigation required."
            }

    elif repair_type == "electrical":

        result = {
            "priority": "Emergency",
            "trade": "Electrician",
            "attendance": "24 Hours",
            "message": "Electrical issue reported."
        }

    elif repair_type == "heating":

        if vulnerable == "yes":

            result = {
                "priority": "Emergency",
                "trade": "Heating Engineer",
                "attendance": "24 Hours",
                "message": "Vulnerable resident without heating."
            }

        else:

            result = {
                "priority": "Urgent",
                "trade": "Heating Engineer",
                "attendance": "48 Hours",
                "message": "Loss of heating reported."
            }

    elif repair_type == "damp":

        result = {
            "priority": "Routine",
            "trade": "Damp Specialist",
            "attendance": "28 Days",
            "message": "Damp and mould inspection required."
        }

    else:

        result = {
            "priority": "Routine",
            "trade": "Roofer",
            "attendance": "28 Days",
            "message": "Roofing issue reported."
        }

    return render_template(
        "result.html",
        result=result
    )