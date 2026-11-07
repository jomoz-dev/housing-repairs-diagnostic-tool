from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/diagnose", methods=["POST"])
def diagnose():

    danger = request.form["danger"]
    unsafe_property = request.form["unsafe_property"]
    vulnerable = request.form["vulnerable"]

    repair_type = request.form["repair_type"]

    active_leak = request.form["active_leak"]
    contained = request.form["contained"]
    electrics_affected = request.form["electrics_affected"]

    sparking = request.form["sparking"]

    burning_smell = request.form["burning_smell"]

    power_loss = request.form["power_loss"]
    # Emergency safety assessment

    if danger == "yes" or unsafe_property == "yes":

        result = {
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
                "trade": "Plumber / Electrician",
                "attendance": "24 Hours",
                "message": "Water is affecting electrical fittings."
            }

        elif active_leak == "yes" and contained == "no":

            result = {
                "priority": "Emergency",
                "trade": "Plumber",
                "attendance": "24 Hours",
                "message": "Active leak cannot be contained."
            }

        elif active_leak == "yes":

            result = {
                "priority": "Urgent",
                "trade": "Plumber",
                "attendance": "48 Hours",
                "message": "Active leak reported."
            }

        else:

            result = {
                "priority": "Routine",
                "trade": "Plumber",
                "attendance": "28 Days",
                "message": "Leak investigation required."
            }

    # Electrical

    elif repair_type == "electrical":

        if sparking == "yes" or burning_smell == "yes":

            result = {
                "priority": "Emergency",
                "trade": "Electrician",
                "attendance": "24 Hours",
                "message": "Potential electrical safety risk identified."
            }

        elif power_loss == "yes":

            result = {
                "priority": "Urgent",
                "trade": "Electrician",
                "attendance": "48 Hours",
                "message": "Complete loss of power reported."
            }

        else:

            result = {
                "priority": "Routine",
                "trade": "Electrician",
                "attendance": "28 Days",
                "message": "Electrical inspection required."
            }
    # Heating

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

    # Damp & Mould

    elif repair_type == "damp":

        result = {
            "priority": "Routine",
            "trade": "Damp Specialist",
            "attendance": "28 Days",
            "message": "Damp and mould inspection required."
        }

    # Roofing

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


if __name__ == "__main__":
    app.run(debug=True)