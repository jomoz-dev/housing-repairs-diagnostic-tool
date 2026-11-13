def diagnose_repair(answers):
    """Apply repairs business rules and return priority, trade and attendance."""

    danger = answers.get("danger", "no")
    unsafe_property = answers.get("unsafe_property", "no")
    vulnerable = answers.get("vulnerable", "no")
    repair_type = answers["repair_type"]

    active_leak = answers.get("active_leak", "no")
    contained = answers.get("contained", "yes")
    electrics_affected = answers.get("electrics_affected", "no")

    sparking = answers.get("sparking", "no")
    burning_smell = answers.get("burning_smell", "no")
    power_loss = answers.get("power_loss", "no")

    heating_failed = answers.get("heating_failed", "no")
    hot_water = answers.get("hot_water", "no")

    visible_mould = answers.get("visible_mould", "no")
    long_term_issue = answers.get("long_term_issue", "no")
    children_present = answers.get("children_present", "no")
    respiratory_condition = answers.get("respiratory_condition", "no")

    water_entry = answers.get("water_entry", "no")
    structural_damage = answers.get("structural_damage", "no")
    roof_electrics = answers.get("roof_electrics", "no")

    security_risk = answers.get("security_risk", "no")
    door_secured = answers.get("door_secured", "yes")
    window_closed = answers.get("window_closed", "yes")

    if danger == "yes" or unsafe_property == "yes":
        return {
            "repair_type": repair_type,
            "priority": "Emergency",
            "trade": "Emergency Contractor",
            "attendance": "Within 24 Hours",
            "message": "Potential health and safety risk identified."
        }

    if repair_type == "water_leak":
        if electrics_affected == "yes":
            return {
                "repair_type": repair_type,
                "priority": "Emergency",
                "trade": "Plumber / Electrician",
                "attendance": "2-4  Hours",
                "message": "Water is affecting electrical fittings."
            }
        if active_leak == "yes" and contained == "no":
            return {
                "repair_type": repair_type,
                "priority": "Emergency",
                "trade": "Plumber",
                "attendance": "24 Hours",
                "message": "Active leak cannot be contained."
            }
        if active_leak == "yes":
            return {
                "repair_type": repair_type,
                "priority": "Urgent",
                "trade": "Plumber",
                "attendance": "72 Hours",
                "message": "Active leak reported."
            }
        return {
            "repair_type": repair_type,
            "priority": "Routine",
            "trade": "Plumber",
            "attendance": "28 Days",
            "message": "Leak investigation required."
        }

    if repair_type == "electrical":
        if sparking == "yes" or burning_smell == "yes":
            return {
                "repair_type": repair_type,
                "priority": "Emergency",
                "trade": "Electrician",
                "attendance": "2-4 Hours",
                "message": "Potential electrical safety risk identified."
            }
        if power_loss == "yes":
            return {
                "repair_type": repair_type,
                "priority": "Urgent",
                "trade": "Electrician",
                "attendance": "24 Hours",
                "message": "Complete loss of power reported."
            }
        return {
            "repair_type": repair_type,
            "priority": "Routine",
            "trade": "Electrician",
            "attendance": "28 Days",
            "message": "Electrical inspection required."
        }

    if repair_type == "heating":
        if heating_failed == "yes" and vulnerable == "yes":
            return {
                "repair_type": repair_type,
                "priority": "Emergency",
                "trade": "Heating Engineer",
                "attendance": "4 Hours",
                "message": "Vulnerable resident without heating."
            }
        if heating_failed == "yes":
            return {
                "repair_type": repair_type,
                "priority": "Urgent",
                "trade": "Heating Engineer",
                "attendance": "24 Hours",
                "message": "Heating failure reported."
            }
        if hot_water == "yes":
            return {
                "repair_type": repair_type,
                "priority": "Urgent",
                "trade": "Heating Engineer",
                "attendance": "24 Hours",
                "message": "Loss of hot water reported."
            }
        return {
            "repair_type": repair_type,
            "priority": "Routine",
            "trade": "Heating Engineer",
            "attendance": "28 Days",
            "message": "Heating inspection required."
        }

    if repair_type == "damp_mould":
        if visible_mould == "yes" and respiratory_condition == "yes":
            return {
                "repair_type": repair_type,
                "priority": "Urgent",
                "trade": "Damp Specialist",
                "attendance": "7 Days",
                "message": "Visible mould and respiratory risk identified."
            }
        if visible_mould == "yes" and children_present == "yes":
            return {
                "repair_type": repair_type,
                "priority": "Urgent",
                "trade": "Damp Specialist",
                "attendance": "7 Days",
                "message": "Visible mould affecting vulnerable occupants."
            }
        if visible_mould == "yes" and long_term_issue == "yes":
            return {
                "repair_type": repair_type,
                "priority": "Urgent",
                "trade": "Damp Specialist",
                "attendance": "7 Days",
                "message": "Long-term damp and mould issue reported."
            }
        return {
            "repair_type": repair_type,
            "priority": "Routine",
            "trade": "Damp Specialist",
            "attendance": "28 Days",
            "message": "Damp inspection required."
        }

    if repair_type == "roofing":
        if water_entry == "yes" and roof_electrics == "yes":
            return {
                "repair_type": repair_type,
                "priority": "Emergency",
                "trade": "Roofer",
                "attendance": "2-4 Hours",
                "message": "Water ingress affecting electrics."
            }
        if water_entry == "yes":
            return {
                "repair_type": repair_type,
                "priority": "Urgent",
                "trade": "Roofer",
                "attendance": "7 Days",
                "message": "Water entering property."
            }
        if structural_damage == "yes":
            return {
                "repair_type": repair_type,
                "priority": "Urgent",
                "trade": "Roofer",
                "attendance": "7 Days",
                "message": "Structural roof damage reported."
            }
        return {
            "repair_type": repair_type,
            "priority": "Routine",
            "trade": "Roofer",
            "attendance": "28 Days",
            "message": "Roof inspection required."
        }

    if repair_type == "doors_windows":
        if security_risk == "yes":
            return {
                "repair_type": repair_type,
                "priority": "Emergency",
                "trade": "Locksmith",
                "attendance": "24 Hours",
                "message": "Property security compromised."
            }
        if door_secured == "no":
            return {
                "repair_type": repair_type,
                "priority": "Urgent",
                "trade": "Locksmith",
                "attendance": "48 Hours",
                "message": "Door cannot be secured."
            }
        if window_closed == "no":
            return {
                "repair_type": repair_type,
                "priority": "Urgent",
                "trade": "Joiner",
                "attendance": "48 Hours",
                "message": "Window cannot be closed."
            }
        return {
            "repair_type": repair_type,
            "priority": "Routine",
            "trade": "Joiner",
            "attendance": "28 Days",
            "message": "Minor door or window repair required."
        }

    return {
        "repair_type": repair_type,
        "priority": "Routine",
        "trade": "Inspection",
        "attendance": "28 Days",
        "message": "Repair type requires further assessment."
    }
