from datetime import date

from app import record_in_date_range


def test_no_dates_keeps_all_records():
    assert record_in_date_range("13/11/2026 02:57", None, None) is True


def test_from_date_excludes_earlier_records():
    assert record_in_date_range(
        "12/11/2026 09:00",
        date(2026, 11, 13),
        None,
    ) is False


def test_to_date_excludes_later_records():
    assert record_in_date_range(
        "14/11/2026 09:00",
        None,
        date(2026, 11, 13),
    ) is False


def test_inclusive_range_keeps_matching_day():
    assert record_in_date_range(
        "13/11/2026 02:57",
        date(2026, 11, 13),
        date(2026, 11, 13),
    ) is True


def test_missing_stored_date_is_excluded_when_filtering():
    assert record_in_date_range(
        None,
        date(2026, 11, 1),
        None,
    ) is False
