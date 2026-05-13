import pytest
from nldate import parse
from datetime import date, timedelta

def test_no_args_provided():
    with pytest.raises(TypeError):
        parse()

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
