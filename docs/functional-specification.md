# Functional Specification

## Overview

The application uses rule\-based decision trees to evaluate repair requests.

Each repair workflow contains a defined set of questions and business rules.

## Workflow

1. User selects repair category.
2. User completes assessment questions.
3. System evaluates business rules.
4. Priority is assigned.
5. Trade recommendation is generated.
6. Assessment is saved to database.
7. Reference number is generated.
8. Results are displayed.

## Priority Categories

### Emergency

Response required within emergency service levels.

### Urgent

Response required within urgent service levels.

### Routine

Response required within routine service levels.

## Reporting Functions

- Assessment History
- Dashboard Analytics
- Search by Reference
- CSV Export
- Priority Filtering
- Repair\-Type Filtering

## Data Storage

Assessment records are stored within an SQLite database.

The database retains:

- Reference Number
- Repair Type
- Priority
- Trade
- Attendance Time
- Assessment Notes
- Assessment Date

