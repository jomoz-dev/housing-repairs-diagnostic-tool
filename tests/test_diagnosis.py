from diagnosis import diagnose_repair


def test_safety_override_is_emergency():
    result = diagnose_repair(
        {"repair_type": "water_leak", "danger": "yes"}
    )
    assert result["priority"] == "Emergency"
    assert result["trade"] == "Emergency Contractor"


def test_leak_affecting_electrics_is_emergency():
    result = diagnose_repair(
        {
            "repair_type": "water_leak",
            "electrics_affected": "yes",
        }
    )
    assert result["priority"] == "Emergency"
    assert result["trade"] == "Plumber / Electrician"
    assert result["attendance"] == "2-4  Hours"


def test_uncontained_leak_is_emergency():
    result = diagnose_repair(
        {
            "repair_type": "water_leak",
            "active_leak": "yes",
            "contained": "no",
        }
    )
    assert result["priority"] == "Emergency"
    assert result["attendance"] == "24 Hours"


def test_contained_active_leak_is_urgent():
    result = diagnose_repair(
        {
            "repair_type": "water_leak",
            "active_leak": "yes",
            "contained": "yes",
        }
    )
    assert result["priority"] == "Urgent"
    assert result["trade"] == "Plumber"


def test_sparking_electrical_is_emergency():
    result = diagnose_repair(
        {"repair_type": "electrical", "sparking": "yes"}
    )
    assert result["priority"] == "Emergency"
    assert result["trade"] == "Electrician"


def test_power_loss_is_urgent():
    result = diagnose_repair(
        {"repair_type": "electrical", "power_loss": "yes"}
    )
    assert result["priority"] == "Urgent"
    assert result["attendance"] == "24 Hours"


def test_heating_failure_with_vulnerable_resident_is_emergency():
    result = diagnose_repair(
        {
            "repair_type": "heating",
            "heating_failed": "yes",
            "vulnerable": "yes",
        }
    )
    assert result["priority"] == "Emergency"
    assert result["attendance"] == "4 Hours"
    assert result["trade"] == "Heating Engineer"


def test_heating_failure_without_vulnerability_is_urgent():
    result = diagnose_repair(
        {"repair_type": "heating", "heating_failed": "yes"}
    )
    assert result["priority"] == "Urgent"
    assert result["attendance"] == "24 Hours"


def test_visible_mould_with_respiratory_condition_is_urgent():
    result = diagnose_repair(
        {
            "repair_type": "damp_mould",
            "visible_mould": "yes",
            "respiratory_condition": "yes",
        }
    )
    assert result["priority"] == "Urgent"
    assert result["attendance"] == "7 Days"
    assert result["trade"] == "Damp Specialist"


def test_visible_mould_with_children_under_five_is_urgent():
    result = diagnose_repair(
        {
            "repair_type": "damp_mould",
            "visible_mould": "yes",
            "children_present": "yes",
        }
    )
    assert result["priority"] == "Urgent"
    assert result["attendance"] == "7 Days"


def test_damp_with_no_risk_flags_is_routine():
    result = diagnose_repair({"repair_type": "damp_mould"})
    assert result["priority"] == "Routine"
    assert result["attendance"] == "28 Days"


def test_roof_water_and_electrics_is_emergency():
    result = diagnose_repair(
        {
            "repair_type": "roofing",
            "water_entry": "yes",
            "roof_electrics": "yes",
        }
    )
    assert result["priority"] == "Emergency"
    assert result["trade"] == "Roofer"


def test_security_risk_is_emergency_locksmith():
    result = diagnose_repair(
        {
            "repair_type": "doors_windows",
            "security_risk": "yes",
        }
    )
    assert result["priority"] == "Emergency"
    assert result["trade"] == "Locksmith"


def test_unsecured_door_is_urgent_locksmith():
    result = diagnose_repair(
        {
            "repair_type": "doors_windows",
            "door_secured": "no",
        }
    )
    assert result["priority"] == "Urgent"
    assert result["trade"] == "Locksmith"
    assert result["attendance"] == "48 Hours"


def test_window_cannot_close_is_urgent_joiner():
    result = diagnose_repair(
        {
            "repair_type": "doors_windows",
            "window_closed": "no",
        }
    )
    assert result["priority"] == "Urgent"
    assert result["trade"] == "Joiner"
