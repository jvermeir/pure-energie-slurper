from datetime import datetime, timedelta
from pathlib import Path

from data_loader import should_continue, find_end_date


def test_should_continue():
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    three_weeks_ago = today - timedelta(days=21)
    two_weeks_ago = today - timedelta(days=14)
    thirteen_days_ago = today - timedelta(days=13)
    assert (should_continue(three_weeks_ago, yesterday), True)
    assert (should_continue(two_weeks_ago, yesterday), True)
    assert (should_continue(yesterday, yesterday), False)
    assert (should_continue(thirteen_days_ago, yesterday), False)


def test_find_end_date():
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    three_weeks_ago = today - timedelta(days=21)
    one_week_ago = today - timedelta(days=7)
    assert (find_end_date(yesterday), yesterday)
    assert (find_end_date(today), yesterday)
    assert (find_end_date(three_weeks_ago), one_week_ago)
    assert (find_end_date(one_week_ago), yesterday)
