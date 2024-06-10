from datetime import datetime

import properties
from database import get_latest_date_from_db, get_data_by_year, get_data_by_month, get_data_by_day, get_data_by_hour


def data_by_hour(start_time, end_time):
    return get_data_by_hour(start_time, end_time)


def data_by_day(start_time, end_time):
    return get_data_by_day(start_time, end_time)


def data_by_month(start_time, end_time):
    return get_data_by_month(start_time, end_time)


def data_by_year(start_time, end_time):
    return get_data_by_year(start_time, end_time)


def get_latest_date():
    date = datetime.strptime(properties.start_of_data, properties.DATE_FORMAT).date()
    result = get_latest_date_from_db()
    if result is not None:
        # TODO: this would be the latest date for which we've got non-0 data in the database.
        # we're reading this data again when renewing to make sure the query returns data for at least one day
        # the api throws an exception if you ask for data that doesn't exist (argh!)
        max_period, = result
        date = datetime.strptime(str.split(max_period, ' ')[0], properties.DATE_FORMAT).date()
    return date
