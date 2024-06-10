from datetime import datetime

import properties
from dataservice import get_latest_date, data_by_month, data_by_year


def test_get_latest_date_returns_a_date(mocker):
    def get_latest_date_returns_a_date():
        return ('2024-07-08 18:59:00',)

    mocker.patch('dataservice.get_latest_date_from_db', get_latest_date_returns_a_date)
    assert get_latest_date() == datetime(2024, 7, 8).date()


def test_get_latest_date_returns_a_default(mocker):
    def get_latest_date_returns_none():
        return None

    mocker.patch('dataservice.get_latest_date_from_db', get_latest_date_returns_none)
    assert get_latest_date() == datetime.strptime(properties.start_of_data, properties.DATE_FORMAT).date()


def test_data_by_year(mocker):
    def get_data_by_year(start_time, end_time):
        return [('2023', 1602.852, 764.511, 838.341, 832.42, 3422.971)]

    mocker.setattr('dataservice.get_data_by_year', get_data_by_year)
    assert data_by_year('2023-01-01', '2024-01-01') == get_data_by_year


def test_data_by_month(mocker):
    def get_data_by_month_patch():
        return [('2023', '12', 1602.852, 764.511, 838.341, 832.42, 3422.971)]

    mocker.patch('dataservice.get_data_by_month', return_value=get_data_by_month_patch)
    assert data_by_month('2023-01-01', '2024-01-01') == get_data_by_month_patch


def test_data_by_year(mocker):
    def get_data_by_year(start_time, end_time):
        return [('2023', 1602.852, 764.511, 838.341, 832.42, 3422.971)]

    mocker.patch('dataservice.get_data_by_year', get_data_by_year)
    assert data_by_year('2023-01-01', '2024-01-01') == [('2023', 1602.852, 764.511, 838.341, 832.42, 3422.971)]
