from datetime import datetime, timedelta
from pathlib import Path

from data_loader import should_continue, find_end_date, find_latest_data_file_name


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


def test_find_latest_data_file_name(mocker):
    empty_folder = Path(__file__).parent.joinpath('emptyDataFolder')
    mocker.patch("data_loader.DATA_ROOT_FOLDER", empty_folder.absolute())
    assert (find_latest_data_file_name(), '2017-11-19.csv')
    non_empty_folder = Path(__file__).parent.joinpath('nonEmptyDataFolder')

    mocker.patch("data_loader.DATA_ROOT_FOLDER", non_empty_folder.absolute())
    assert (find_latest_data_file_name(), '2024-05-27.csv')
