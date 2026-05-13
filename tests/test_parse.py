import pytest
from nldate import parse
from datetime import date, timedelta

def test_no_args_provided():
    with pytest.raises(TypeError):
        parse()

# Testing today, yesterday, tomorrow
def test_today_date_provided():
    assert parse(s = "today", today = date(2025, 5, 12)) == date(2025, 5, 12)

def test_today_date_not_provide():
    assert parse(s = "today") == date.today()

def test_yesterday_date_provided():
    assert parse(s = "yesterday", today = date(2024, 4, 1)) == date(2024, 3, 31)

def test_yesterday_date_not_provided():
    assert parse(s = "yesterday") == date.today() - timedelta(days = 1)

def test_tomorrow_date_provided():
    assert parse(s = "tomorrow", today = date(1998, 12, 31)) == date(1999, 1, 1)

# Testing "X days" difference inputs
def test_in_X_days():
    assert parse(s = "in 10 days", today = date(2025, 5, 12)) == date(2025, 5, 22)

def test_X_days_ago():
    assert parse(s = "10 days ago") == date.today() - timedelta(days = 10)

# Testing inputs that tell a specific weekday relative to today
"""
def test_next_monday_from_monday():
    assert parse(s = "next Monday",
                 today = date(2025, 5, 12)) == date(2025, 5, 18)

def test_next_monday_from_friday():
    assert parse(s = "next Monday",
                 today = date(2025, 5, 12)) == date(2025, 5, 18)

def test_last_friday_from_friday():
    assert parse(s = "last friday ", 
                 today = date(2025, 5, 8)) == date(2025, 5, 1)

def test_last_friday_from_saturday():
    assert parse(s = "last  friday",
                 today = date(2025, 5, 9)) == date(2025, 5, 1)
"""

# Testing inputs that write out the month in English
def test_full_month_name_mmddyy():
    assert parse("December 1st, 2025") == date(2025, 12, 1)

def test_short_month_name_mmddyy():
    assert parse("Jan 2, 2026") == date(2026, 1, 2)

def test_short_month_name_mmddyy_no_comma():
    assert parse("Jan 2 2026") == date(2026, 1, 2)

def test_full_month_name_ddmmyy():
    assert parse("1 January 2024") == date(2024, 1, 1)

def test_short_month_name_ddmmyy():
    assert parse("1 jan 2024") == date(2024, 1, 1)

def test_1st():
    assert parse("Feb 1st, 2025") == date(2025, 2, 1)

def test_1st_no_comma():
    assert parse("February 1st, 2025") == date(2025, 2, 1)

def test_2nd():
    assert parse("dec 2nd, 2025") == date(2025, 12, 2)

def test_3rd():
    assert parse("dec 3rd 2025") == date(2025, 12, 3)

def test_Xth():
    assert parse("DeCEMBer 31 2025") == date(2025, 12, 31)

# Testing inputs that combine time difference and months written out
def test_days_before_dec_1st():
    assert parse("5 days before December 1st, 2025") == date(2025, 11, 26)

def test_days_after_dec_1():
    assert parse("2 days after dec 1 2025") == date(2025, 12, 3)

def test_years_before():
    assert parse("1 year before January 1, 2025") == date(2024, 1, 1)

def test_year_months_before():
    assert parse("1 year and 2 months before yesterday",
                 date(2025, 5, 12)) == date(2024, 3, 11)

def test_year_months_after():
    assert parse("1 year and 2 months after yesterday",
                 date(2025, 5, 12)) == date(2026, 7, 11)

def test_year_months_after_dec_1():
    assert parse("1 year and 2 months after May 11, 2025") == date(2026, 7, 11)
