from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/diagnose", methods=["POST"])
def diagnose():

    danger = request.form["danger"]
    unsafe_property = request.form["unsafe_property"]
    repair_type = request.form["repair_type"]

    if danger == "yes" or unsafe_property == "yes":

        result = {
            "priority": "Emergency",
            "trade": "Emergency Contractor",
            "attendance": "Within 24 Hours",
            "message": "Potential health and safety risk identified."
        }

    elif repair_type == "water_leak":

        result = {
            "priority": "Urgent",
            "trade": "Plumber",
            "attendance": "48 Hours",
            "message": "Water leak requires investigation."
        }

    elif repair_type == "electrical":

        result = {
            "priority": "Emergency",
            "trade": "Electrician",
            "attendance": "24 Hours",
            "message": "Electrical issues should be assessed promptly."
        }

    elif repair_type == "heating":

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
            "message": "Inspection required."
        }

    else:

        result = {
            "priority": "Routine",
            "trade": "Roofer",
            "attendance": "28 Days",
            "message": "Roofing issue logged."
        }

    return render_template(
        "result.html",
        result=result
    )


if __name__ == "__main__":
    app.run(debug=True)