from datetime import date, timedelta
import re

MONTHS = {
    "january": 1,
    "jan": 1,
    "february": 2,
    "feb": 2,
    "march": 3,
    "mar": 3,
    "april": 4,
    "apr": 4,
    "may": 5,
    "june": 6,
    "jun": 6,
    "july": 7,
    "jul": 7,
    "august": 8,
    "aug": 8,
    "september": 9,
    "sep": 9,
    "sept": 9,
    "october": 10,
    "oct": 10,
    "november": 11,
    "nov": 11,
    "december": 12,
    "dec": 12,
}


# Helper Functions
def _clean_day(day_str: str) -> int:
    return int(re.sub(r"(st|nd|rd|th)", "", day_str))


def _parse_absolute_date(s: str) -> date | None:

    # allow for dates in yyyy-mm-dd format
    iso_match = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", s.strip())
    if iso_match:
            year = int(iso_match.group(1))
            month = int(iso_match.group(2))
            day = int(iso_match.group(3))
            return date(year, month, day)

    # extract year
    year_match = re.search(r"\b(20\d{2})\b", s)
    if not year_match:
        return None
    year = int(year_match.group(1))

    # extract month
    month_match = re.search(
        r"\b(january|february|march|april|may|june|july|august|"
        r"september|october|november|december|"
        r"jan|feb|mar|apr|jun|jul|aug|sep|sept|oct|nov|dec)\b",
        s,
    )
    if not month_match:
        return None
    month = MONTHS[month_match.group(1)]

    # extract day (supports 1, 1st, 31st, etc.)
    day_match = re.search(r"\b(\d{1,2}(?:st|nd|rd|th)?)\b", s)
    if not day_match:
        return None
    day = _clean_day(day_match.group(1))

    return date(year, month, day)


def _resolve_anchor(s: str, today: date) -> date:
    s = s.strip().lower()

    if s == "today":
        return today

    if s == "yesterday":
        return today - timedelta(days=1)

    if s == "tomorrow":
        return today + timedelta(days=1)

    absolute = _parse_absolute_date(s)
    if absolute:
        return absolute

    raise ValueError(f"Unsupported anchor date: {s}")


def _parse_relative_expression(s: str, today: date) -> date | None:
    match = re.match(r"(.+)\s+(before|after)\s+(.+)", s)

    if not match:
        return None

    duration_str = match.group(1)
    direction = match.group(2)
    anchor_str = match.group(3)

    duration = _parse_duration(duration_str)
    anchor = _resolve_anchor(anchor_str, today)

    sign = -1 if direction == "before" else 1

    result = anchor

    # Apply years/months first (calendar-aware)
    if duration["years"]:
        result = _add_years(result, sign * duration["years"])

    if duration["months"]:
        result = _add_months(result, sign * duration["months"])

    # Apply days last
    if duration["days"]:
        result = result + timedelta(days=sign * duration["days"])

    return result


def _add_months(d: date, months: int) -> date:
    month = d.month - 1 + months
    year = d.year + month // 12
    month = month % 12 + 1

    days_in_month = [
        31,
        29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28,
        31,
        30,
        31,
        30,
        31,
        31,
        30,
        31,
        30,
        31,
    ]

    day = min(d.day, days_in_month[month - 1])

    return date(year, month, day)


def _add_years(d: date, years: int) -> date:
    try:
        return d.replace(year=d.year + years)
    except ValueError:
        # Feb 29 -> Feb 28 fallback
        return d.replace(month=2, day=28, year=d.year + years)


def _parse_duration(s: str) -> dict[str, int]:
    parts = re.findall(r"(\d+)\s+(days?|months?|years?)", s)

    if not parts:
        raise ValueError("Invalid duration")

    duration = {
        "days": 0,
        "months": 0,
        "years": 0,
    }

    for value, unit in parts:
        value = int(value)

        if unit.startswith("day"):
            duration["days"] += value
        elif unit.startswith("month"):
            duration["months"] += value
        elif unit.startswith("year"):
            duration["years"] += value

    return duration


# Main Function
def parse(s: str, today: date | None = None) -> date:
    if today is None:
        today = date.today()

    s = s.strip().lower()
    s = re.sub(r"\s+", " ", s)

    if s == "today":
        return today
    if s == "yesterday":
        return today - timedelta(days=1)
    if s == "tomorrow":
        return today + timedelta(days=1)

    # Input includes number of days difference, written as a scalar
    match = re.match(r"in (\d+) days", s)
    if match:
        days = int(match.group(1))
        return today + timedelta(days=days)

    match = re.match(r"(\d+) days ago", s)
    if match:
        days = int(match.group(1))
        return today - timedelta(days=days)

    # Input describes weekdays relative to today
    WEEKDAYS = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6,
    }

    match = re.match(
        r"(next|last)\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)", s
    )
    if match:
        direction = match.group(1)
        weekday = WEEKDAYS[match.group(2)]

        current_weekday = today.weekday()

        if direction == "next":
            days_ahead = (weekday - current_weekday + 7) % 7
            if days_ahead == 0:
                days_ahead = 7
            return today + timedelta(days=days_ahead)

        if direction == "last":
            days_back = (current_weekday - weekday + 7) % 7
            if days_back == 0:
                days_back = 7
            return today - timedelta(days=days_back)

    # Input includes years, months, days and month written out
    result = _parse_relative_expression(s, today)
    if result is not None:
        return result

    # Input is solely date with month written out
    result = _parse_absolute_date(s)
    if result is not None:
        return result

    raise ValueError(f"Unsupported date expression: {s}")
