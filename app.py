from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/diagnose", methods=["POST"])
def diagnose():

    repair_type = request.form["repair_type"]

    if repair_type == "heating":
        result = "Heating Repair"

    elif repair_type == "water_leak":
        result = "Water Leak"

    elif repair_type == "electrical":
        result = "Electrical Repair"

    elif repair_type == "damp":
        result = "Damp & Mould"

    else:
        result = "Roofing"

    return render_template(
        "result.html",
        result=result
    )


if __name__ == "__main__":
    app.run(debug=True)
