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
                "attendance": "2-4  Hours",
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
                "attendance": "72 Hours",
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
                "attendance": "2-4 Hours",
                "message": "Potential electrical safety risk identified."
            }

        elif power_loss == "yes":

            result = {
                "priority": "Urgent",
                "trade": "Electrician",
                "attendance": "24 Hours",
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

        if heating_failed == "yes" and vulnerable == "yes":

            result = {
                "priority": "Emergency",
                "trade": "Heating Engineer",
                "attendance": "4 Hours",
                "message": "Vulnerable resident without heating."
            }

        elif heating_failed == "yes":

            result = {
                "priority": "Urgent",
                "trade": "Heating Engineer",
                "attendance": "24 Hours",
                "message": "Heating failure reported."
            }

        elif hot_water == "yes":

            result = {
                "priority": "Urgent",
                "trade": "Heating Engineer",
                "attendance": "24 Hours",
                "message": "Loss of hot water reported."
            }

        else:

            result = {
                "priority": "Routine",
                "trade": "Heating Engineer",
                "attendance": "28 Days",
                "message": "Heating inspection required."
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