import matplotlib.pyplot as plt
import numpy as np

from database import get_total_by_year, get_hourly


def get_total_usage(verbruik_data):
    year, total_usage, total_usage_day, total_usage_night, total_cost, redelivery = verbruik_data[1]
    return total_usage


def get_total_usage_by_day(verbruik_data):
    year, month, day, total_usage, total_usage_day, total_usage_night, total_cost, redelivery = verbruik_data[1]
    return total_usage


def get_total_usage_by_hour(verbruik_data):
    year, month, day, hour, total_usage, total_usage_day, total_usage_night, total_cost, redelivery = verbruik_data[1]
    return total_usage


def get_redelivery(verbruik_data):
    year, total_usage, total_usage_day, total_usage_night, total_cost, redelivery = verbruik_data[1]
    return redelivery


def get_redelivery_by_day(verbruik_data):
    year, month, day, total_usage, total_usage_day, total_usage_night, total_cost, redelivery = verbruik_data[1]
    return redelivery


def get_redelivery_by_hour(verbruik_data):
    year, month, day, hour, total_usage, total_usage_day, total_usage_night, total_cost, redelivery = verbruik_data[1]
    return redelivery


def get_years(verbruik_data):
    year, total_usage, total_usage_day, total_usage_night, total_cost, redelivery = verbruik_data[1]
    return year


def graph_by_year():
    verbruik_data = get_total_by_year()
    years = [get_years(data) for data in enumerate(verbruik_data)]
    total_usage = [get_total_usage(data) for data in enumerate(verbruik_data)]
    redelivery = [get_redelivery(data) for data in enumerate(verbruik_data)]
    net = [get_total_usage(data) - get_redelivery(data) for data in enumerate(verbruik_data)]

    time_axis = np.array(years)
    total_usage_graph = np.array(total_usage)
    redelivery_graph = np.array(redelivery)
    net_graph = np.array(net)
    plt.plot(time_axis, total_usage_graph, label='Total')
    plt.plot(time_axis, redelivery_graph, label='Redelivery')
    plt.plot(time_axis, net_graph, label='Net')
    plt.xlabel('Year')
    plt.ylabel('kWh')
    plt.legend(plt.gca().lines, ['total', 'redelivery', 'net'])
    plt.show()


def graph_by_day(year, month, day):
    verbruik_data = get_hourly(year, month, day)
    hours = range(0, 24)
    total_usage = [get_total_usage_by_hour(data) for data in enumerate(verbruik_data)]
    redelivery = [get_redelivery_by_hour(data) for data in enumerate(verbruik_data)]
    net = [get_total_usage_by_hour(data) - get_redelivery_by_hour(data) for data in enumerate(verbruik_data)]

    time_axis = np.array(hours)
    total_usage_graph = np.array(total_usage)
    redelivery_graph = np.array(redelivery)
    net_graph = np.array(net)
    plt.plot(time_axis, total_usage_graph, label='Total')
    plt.plot(time_axis, redelivery_graph, label='Redelivery')
    plt.plot(time_axis, net_graph, label='Net')
    plt.xlabel('Hour')
    plt.ylabel('kWh')
    plt.legend(plt.gca().lines, ['total', 'redelivery', 'net'])
    plt.show()


def graph(start_date, end_date, aggregation_level):
    print('TODO: implement graph')