import locale
import re
import sqlite3
from datetime import datetime
from pathlib import Path

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


def float_from_dutch_formated_string(s):
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
            record = [key, parts[0], hour, day, month, year, float_from_dutch_formated_string(parts[1]),
                      float_from_dutch_formated_string(parts[2]),
                      float_from_dutch_formated_string(parts[3]), float_from_dutch_formated_string(parts[4]), float_from_dutch_formated_string(parts[5])]
            update_row(record)


def get_data_by_hour(start_time, end_time):
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
    return cur.fetchall()


def get_data_by_day(start_time, end_time):
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
    return cur.fetchall()


def get_data_by_month(start_time, end_time):
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
    return cur.fetchall()


def get_data_by_year(end_time, start_time):
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
    return cur.fetchall()


def get_latest_date_from_db():
    with sqlite3.connect(DATABASE_FILE) as conn:
        cur = conn.cursor()
        cur.execute(f'''
                select max(period) max_period
                from {VERBRUIK_TABLE}
                where total_usage > 0''')
        return cur.fetchone()
