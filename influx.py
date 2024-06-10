from influxdb_client import InfluxDBClient, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS

import properties
from database import convert_interval_to_date, float_from_dutch_formated_string


class InfluxClient:
    def __init__(self):
        self._org = properties.influx_org
        self._bucket = properties.influx_bucket
        self._client = InfluxDBClient(url=properties.influx_url, token=properties.influx_token)

    def write_data(self, data, write_option=SYNCHRONOUS):
        write_api = self._client.write_api(write_option)
        write_api.write(self._bucket, self._org, data, write_precision=WritePrecision.S)


IC = InfluxClient()


def create_influx_record(record):
    key, period, year, month, day, hour, total_usage, total_usage_day, total_usage_night, total_cost, redelivery = record
    data = [
        {
            "measurement": "verbruik",
            "tags": {"verbruik": "power consumption per hour"},
            "fields": {
                "period": period,
                "year": year,
                "month": month,
                "day": day,
                "hour": hour,
                "total_usage": total_usage,
                "total_usage_day": total_usage_day,
                "total_usage_night": total_usage_night,
                "total_cost": total_cost,
                "redelivery": redelivery,
                "net_usage": total_usage - redelivery
            },
            "time": int(key.timestamp())
        },
    ]
    return data


def update_data(record_set):
    data = record_set.split('\n')
    for line in data:
        if not (line.startswith('Periode') or len(line) == 0):
            parts = line.split(';')
            parts[0] = parts[0].strip('"')
            key = convert_interval_to_date(parts[0])
            hour = key.hour
            day = key.day
            month = key.month
            year = key.year
            record = [key, parts[0], hour, day, month, year, float_from_dutch_formated_string(parts[1]),
                      float_from_dutch_formated_string(parts[2]),
                      float_from_dutch_formated_string(parts[3]), float_from_dutch_formated_string(parts[4]),
                      float_from_dutch_formated_string(parts[5])]
            influx_record = create_influx_record(record)
            IC.write_data(influx_record, write_option=ASYNCHRONOUS)
