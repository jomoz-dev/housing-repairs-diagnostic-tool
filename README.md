# Housing Repairs Diagnostic Tool

## Overview

The Housing Repairs Diagnostic Tool is a Python Flask web application for customer service advisors, housing officers and repairs teams.

It uses guided questions and decision-tree rules to diagnose a reported repair, set a priority, recommend a contractor trade, and record the assessment for later review.

This project comes from real-world work in housing repairs and neighbourhood services. It is also a portfolio piece for a move into business systems analysis, application support, and software development.

---

## What the current version does

An advisor selects a repair type, answers a short set of questions, and receives:

- A unique assessment reference (`HR-YYYYMMDD-HHMMSS`)
- Priority: Emergency, Urgent, or Routine
- Recommended trade
- Target attendance timescale
- Assessment notes

Each outcome is stored in SQLite. History and a dashboard summarise volume by priority and repair type.

### Repair workflows

| Repair type | Questions used | Typical trades |
| --- | --- | --- |
| Water leak | Active leak, contained, electrics affected | Plumber, Plumber / Electrician |
| Electrical | Sparking, burning smell, power loss | Electrician |
| Heating | Heating failed, hot water unavailable, vulnerable resident | Heating Engineer |
| Damp and mould | Visible mould, issue over 28 days, children under 5, respiratory condition | Damp Specialist |
| Roofing | Water entering property, structural damage, electrics affected | Roofer |
| Doors and windows | Door secured, window closed, security risk | Locksmith, Joiner |

### How triage works

```text
Repair type selected
      |
      v
Guided questions for that trade
      |
      v
Decision-tree rules
      |
      v
Priority + trade + attendance
      |
      v
Result saved (SQLite) → History / Dashboard
```

Examples of the rules:

- Water affecting electrics, sparking, or a burning smell → Emergency
- Uncontained leak, heating failure with a vulnerable resident, or a security risk → Emergency
- Visible mould with children under 5, a respiratory condition, or a long-term issue → Urgent (7 days)
- Door that cannot be secured, or a window that cannot be closed → Urgent
- Inspection-only reports with no high-risk answers → Routine (28 days)

---

## Features in this version

- Repair type selection
- Six decision-tree assessments
- Emergency / urgent / routine classification
- Assessment reference and timestamp
- SQLite assessment history with assessment date
- Dashboard: totals, priority split, most common repair types, and bar charts
- Search by assessment reference
- History filters by priority and repair type
- CSV export of assessment records

---

## Technologies

- Python
- Flask
- HTML / CSS
- SQLite

---

## How to run

```text
python database.py
python app.py
```

Then open `http://127.0.0.1:5000/` in a browser.

`database.py` creates the `assessments` table if it does not already exist.

Run the business-rule tests with:

```text
python -m pytest
```

---

## Business problem

Housing organisations often rely on advisor knowledge and manual procedures to diagnose repairs. That can lead to inconsistent diagnoses, incorrect trade allocation, extra cost, repeat contact, and poor satisfaction.

This tool standardises triage so the same answers produce the same priority, trade, and timescale.

---

## Current development progress

### Completed

- Flask application structure
- GitHub repository
- Repair type selection and results page
- Decision trees for water leak, electrical, heating, damp and mould, roofing, and doors and windows
- Emergency / urgent / routine classification
- SQLite storage and assessment references
- History page with priority and repair-type filters
- Search by reference
- CSV export
- Reporting dashboard

### Planned

- User authentication and audit logging
- Resident self-service portal
- Contractor tracking
- PostgreSQL
- Power BI / richer analytics
- Django rewrite (if the product needs a fuller housing application)

---

## Learning objectives

This project is used to practise:

- Python and web development
- Business systems analysis
- Process automation
- Requirements gathering
- Workflow and database design
- Housing repairs domain knowledge

---

## Author

### Jeffrey Omozeghian

Housing professional transitioning into:

- Business systems analysis
- Application support
- Process automation
- Software development

The aim is to show both technical development skill and housing repairs expertise, not a generic calculator or to-do list.
