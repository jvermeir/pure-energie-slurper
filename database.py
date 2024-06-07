import locale
import re
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

import properties

VERBRUIK_TABLE = 'VERBRUIK_PER_UUR'
DATABASE_FILE = (Path(__file__).with_name('data').absolute() / Path('verbruiksdb.db')).as_posix()

create_table_statement: str = f"""CREATE TABLE IF NOT EXISTS {VERBRUIK_TABLE} (
                period TEXT PRIMARY KEY, 
                period_as_string TEXT UNIQUE NOT NULL ,
                hour TEXT,
                day TEXT,
                month TEXT,
                year TEXT,
                total_usage REAL,
                total_usage_day REAL,
                total_usage_night REAL,
                total_cost REAL,
                redelivery REAL
        )"""


# TODO: execute this on startup?
def create_table():
    print('create table')
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(create_table_statement)
        conn.commit()


def update_row(verbruik_per_uur):
    sql = f'''REPLACE INTO {VERBRUIK_TABLE} (
         period, period_as_string, hour, day, month, year, total_usage, total_usage_day, total_usage_night, total_cost, redelivery)
                  VALUES(?,?,?,   ?, ?, ?,   ?, ?, ?,   ?, ?) 
                  '''

    with sqlite3.connect(DATABASE_FILE) as conn:
        cur = conn.cursor()
        cur.execute(sql, verbruik_per_uur)
        conn.commit()
        return cur.lastrowid


def convert_interval_to_date(interval):
    locale.setlocale(locale.LC_TIME, "nl_NL")
    timestamp = re.sub(' tot .*? ', '', interval)
    return datetime.strptime(timestamp, '%H:%M%d %B %Y')


def float_from_string(s):
    return float(s.replace(',', '.'))


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
            record = [key, parts[0], hour, day, month, year, float_from_string(parts[1]),
                      float_from_string(parts[2]),
                      float_from_string(parts[3]), float_from_string(parts[4]), float_from_string(parts[5])]
            update_row(record)


def data_by_hour(start_time, end_time):
    result = []
    with sqlite3.connect(DATABASE_FILE) as conn:
        cur = conn.cursor()
        cur.execute(f'''
                select year,
                month,
                day,
                hour,
                total_usage as total_usage,
                total_usage_day as total_usage_day,
                total_usage_night as total_usage_night,
                total_cost as total_cost,
                redelivery as redelivery 
                from {VERBRUIK_TABLE}
                where period between '{start_time}' and '{end_time}'
                ''')
    rows = cur.fetchall()
    for row in rows:
        result.append(row)
    return result


def data_by_day(start_time, end_time):
    result = []
    with sqlite3.connect(DATABASE_FILE) as conn:
        cur = conn.cursor()
        cur.execute(f'''
                select year,
                month,
                day,
                sum(total_usage) as total_usage,
                sum(total_usage_day) as total_usage_day,
                sum(total_usage_night) as total_usage_night,
                sum(total_cost) as total_cost,
                sum(redelivery) as redelivery
                from {VERBRUIK_TABLE}
                where period between '{start_time}' and '{end_time}'
                group by year, month, day
                order by period''')
    rows = cur.fetchall()
    for row in rows:
        result.append(row)
    return result


def data_by_month(start_time, end_time):
    result = []
    with sqlite3.connect(DATABASE_FILE) as conn:
        cur = conn.cursor()
        cur.execute(f'''
                select year,
                month,
                sum(total_usage) as total_usage,
                sum(total_usage_day) as total_usage_day,
                sum(total_usage_night) as total_usage_night,
                sum(total_cost) as total_cost,
                sum(redelivery) as redelivery
                from {VERBRUIK_TABLE}
                where period between '{start_time}' and '{end_time}'
                group by year, month
                order by period''')
    rows = cur.fetchall()
    for row in rows:
        result.append(row)
    return result


def data_by_year(start_time, end_time):
    result = []
    with sqlite3.connect(DATABASE_FILE) as conn:
        cur = conn.cursor()
        cur.execute(f'''
                select year,
                sum(total_usage) as total_usage,
                sum(total_usage_day) as total_usage_day,
                sum(total_usage_night) as total_usage_night,
                sum(total_cost) as total_cost,
                sum(redelivery) as redelivery
                from {VERBRUIK_TABLE}
                where period between '{start_time}' and '{end_time}'
                group by year
                order by period''')
    rows = cur.fetchall()
    for row in rows:
        result.append(row)
    return result


def get_latest_date():
    date = datetime.strptime(properties.start_of_data, properties.DATE_FORMAT).date()
    with sqlite3.connect(DATABASE_FILE) as conn:
        cur = conn.cursor()
        cur.execute(f'''
                select max(period) max_period
                from {VERBRUIK_TABLE}
                where total_usage > 0''')
        result = cur.fetchone()
        if result is not None:
            # TODO: this would be the latest date for which we've got non-0 data in the database.
            # we're reading this data again when renewing to make sure the query returns data for at least one day
            # the api throws an exception if you ask for data that doesn't exist (argh!)
            max_period, = result
            date = datetime.strptime(str.split(max_period,' ')[0], properties.DATE_FORMAT).date()
    return date
