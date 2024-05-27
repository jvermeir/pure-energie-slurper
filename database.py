import sqlite3
import locale
import re
from datetime import datetime
import os
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


def get_all():
    result = []
    with sqlite3.connect(DATABASE_FILE) as conn:
        cur = conn.cursor()
        cur.execute(f'select * from {VERBRUIK_TABLE}')
        rows = cur.fetchall()
        for row in rows:
            result.append(row)
    return result


def float_from_string(s):
    return float(s.replace(',', '.'))


def load_datafiles():
    data_folder = Path(__file__).with_name('data').absolute()
    # data_folder = Path(__file__).with_name('temp').absolute()
    files = list(filter(lambda file: file.endswith('.csv'), sorted(os.listdir(data_folder))))
    for file in files:
        print(file)
        absolute_file = os.path.join(data_folder, file)
        with open(absolute_file, 'r') as data_file:
            data = data_file.read().split('\n')
            for line in data:
                if not (line.startswith('Periode') or len(line) == 0):
                    parts = line.split(';')
                    parts[0] = parts[0].strip('"')
                    key = convert_interval_to_date(parts[0])
                    hour = key.hour
                    day = key.day
                    month = key.month
                    year = key.year
                    record = [key, parts[0], hour, day, month, year, float_from_string(parts[1]), float_from_string(parts[2]),
                              float_from_string(parts[3]), float_from_string(parts[4]), float_from_string(parts[5])]
                    update_row(record)


def get_total_by_year(year = None):
    result = []
    where_clause = ''
    if year is not None:
        where_clause = f'''where year = {year}'''
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
                {where_clause} 
                group by year''')
    rows = cur.fetchall()
    for row in rows:
        result.append(row)
    return result


def get_total_by_month(year=None, month=None):
    result = []
    where_clause = ''
    if year is not None:
        where_clause = f'''where year = {year} and month = {month}'''
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
                {where_clause} 
                group by year, month''')
    rows = cur.fetchall()
    for row in rows:
        result.append(row)
    return result


def get_total_by_day(year=None, month=None, day=None):
    result = []
    where_clause = ''
    if year is not None:
        where_clause = f'''where year = {year} and month = {month} and day = {day}'''
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
                {where_clause}
                group by year, month, day''')
    rows = cur.fetchall()
    for row in rows:
        result.append(row)
    return result


def get_by_hour(year=None, month=None, day=None, hour=None):
    result = []
    where_clause = ''
    if year is not None:
        where_clause = f'''where year = {year} and month = {month} and day = {day} and hour = {hour}'''
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
                {where_clause}''')
    rows = cur.fetchall()
    for row in rows:
        result.append(row)
    return result


def get_hourly(year=None, month=None, day=None):
    result = []
    where_clause = ''
    if year is not None:
        where_clause = f'''where year = {year} and month = {month} and day = {day}'''
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
                {where_clause}''')
    rows = cur.fetchall()
    for row in rows:
        result.append(row)
    return result
