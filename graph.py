from datetime import datetime, date

import matplotlib.pyplot as plt

import properties
from dataservice import data_by_day, data_by_month, data_by_hour, data_by_year

AGGREGATION_LEVELS = ['year', 'month', 'day', 'hour']


# TODO
# - refactor get_total* functions
# - refactor graph* functions

def get_total_usage_by_year(verbruik_data):
    year, total_usage, total_usage_day, total_usage_night, total_cost, redelivery = verbruik_data[1]
    return total_usage


def get_total_usage_by_hour(verbruik_data):
    year, month, day, hour, total_usage, total_usage_day, total_usage_night, total_cost, redelivery = verbruik_data[1]
    return total_usage


def get_total_usage_by_day(verbruik_data):
    year, month, day, total_usage, total_usage_day, total_usage_night, total_cost, redelivery = verbruik_data[1]
    return total_usage


def get_total_usage_by_month(verbruik_data):
    year, month, total_usage, total_usage_day, total_usage_night, total_cost, redelivery = verbruik_data[1]
    return total_usage


def get_redelivery_by_year(verbruik_data):
    year, total_usage, total_usage_day, total_usage_night, total_cost, redelivery = verbruik_data[1]
    return redelivery


def get_redelivery_by_day(verbruik_data):
    year, month, day, total_usage, total_usage_day, total_usage_night, total_cost, redelivery = verbruik_data[1]
    return redelivery


def get_redelivery_by_month(verbruik_data):
    year, month, total_usage, total_usage_day, total_usage_night, total_cost, redelivery = verbruik_data[1]
    return redelivery


def get_redelivery_by_hour(verbruik_data):
    year, month, day, hour, total_usage, total_usage_day, total_usage_night, total_cost, redelivery = verbruik_data[1]
    return redelivery


def get_years(verbruik_data):
    year, total_usage, total_usage_day, total_usage_night, total_cost, redelivery = verbruik_data[1]
    return year


def get_hours(verbruik_data):
    year, month, day, hour, total_usage, total_usage_day, total_usage_night, total_cost, redelivery = verbruik_data[1]
    return datetime(int(year), int(month), int(day), int(hour), 0, 0)


def get_dates(verbruik_data):
    year, month, day, total_usage, total_usage_day, total_usage_night, total_cost, redelivery = verbruik_data[1]
    return datetime(int(year), int(month), int(day))


def get_months(verbruik_data):
    year, month, total_usage, total_usage_day, total_usage_night, total_cost, redelivery = verbruik_data[1]
    return datetime(int(year), int(month), 1)


def get_default_first_day():
    return datetime.strptime(properties.start_of_data, properties.DATE_FORMAT).date()


def get_first_year_in_data():
    first_day = get_default_first_day()
    date(first_day.year, 1, 1)


def graph(aggregation_level, start_date=None, end_date=None):
    if start_date is None:
        start_date = get_default_first_day()
    if end_date is None:
        end_date = properties.YESTERDAY

    if aggregation_level == 'year':
        graph_year(start_date, end_date)
    elif aggregation_level == 'month':
        graph_month(start_date, end_date)
    elif aggregation_level == 'day':
        graph_day(start_date, end_date)
    elif aggregation_level == 'hour':
        graph_hour(start_date, end_date)

def graph_hour(start_date, end_date):
    verbruik_data = data_by_hour(start_date + ' 00:00:00', end_date + ' 23:59:59')
    dates = [get_hours(data) for data in enumerate(verbruik_data)]

    total_usage = [get_total_usage_by_hour(data) for data in enumerate(verbruik_data)]
    redelivery = [get_redelivery_by_hour(data) for data in enumerate(verbruik_data)]
    net = [get_total_usage_by_hour(data) - get_redelivery_by_hour(data) for data in enumerate(verbruik_data)]

    plt.xticks(rotation=60)
    plt.plot(dates, total_usage)
    plt.plot(dates, redelivery)
    plt.plot(dates, net)
    plt.xlabel('Hour')
    plt.ylabel('kWh')
    plt.tight_layout()
    plt.legend(plt.gca().lines, ['total', 'redelivery', 'net'])

    plt.show()


def graph_day(start_date, end_date):
    verbruik_data = data_by_day(start_date, end_date)
    dates = [get_dates(data) for data in enumerate(verbruik_data)]

    total_usage = [get_total_usage_by_day(data) for data in enumerate(verbruik_data)]
    redelivery = [get_redelivery_by_day(data) for data in enumerate(verbruik_data)]
    net = [get_total_usage_by_day(data) - get_redelivery_by_day(data) for data in enumerate(verbruik_data)]

    plt.xticks(rotation=60)
    plt.plot(dates, total_usage)
    plt.plot(dates, redelivery)
    plt.plot(dates, net)
    plt.xlabel('Day')
    plt.ylabel('kWh')
    plt.tight_layout()
    plt.legend(plt.gca().lines, ['total', 'redelivery', 'net'])

    plt.show()


def graph_month(start_date, end_date):
    verbruik_data = data_by_month(start_date, end_date)
    dates = [get_months(data) for data in enumerate(verbruik_data)]

    total_usage = [get_total_usage_by_month(data) for data in enumerate(verbruik_data)]
    redelivery = [get_redelivery_by_month(data) for data in enumerate(verbruik_data)]
    net = [get_total_usage_by_month(data) - get_redelivery_by_month(data) for data in enumerate(verbruik_data)]

    plt.xticks(rotation=60)
    plt.plot(dates, total_usage)
    plt.plot(dates, redelivery)
    plt.plot(dates, net)
    plt.xlabel('Month')
    plt.ylabel('kWh')
    plt.tight_layout()
    plt.legend(plt.gca().lines, ['total', 'redelivery', 'net'])

    plt.show()


def graph_year(start_date, end_date):
    verbruik_data = data_by_year(start_date, end_date)
    dates = [get_years(data) for data in enumerate(verbruik_data)]

    total_usage = [get_total_usage_by_year(data) for data in enumerate(verbruik_data)]
    redelivery = [get_redelivery_by_year(data) for data in enumerate(verbruik_data)]
    net = [get_total_usage_by_year(data) - get_redelivery_by_year(data) for data in enumerate(verbruik_data)]

    plt.xticks(rotation=60)
    plt.plot(dates, total_usage)
    plt.plot(dates, redelivery)
    plt.plot(dates, net)
    plt.xlabel('Year')
    plt.ylabel('kWh')
    plt.tight_layout()
    plt.legend(plt.gca().lines, ['total', 'redelivery', 'net'])

    plt.show()
