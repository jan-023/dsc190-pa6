import pytest
from nldate import parse
from datetime import date

def test_no_args_provided():
    with pytest.raises(TypeError):
        parse()

def test_today_date_provided():
    assert parse(s = "today", today = date(2025, 5, 12)) == date(2025, 5, 12)

def test_today_date_not_provide():
    assert parse(s = "today") == date.today()

