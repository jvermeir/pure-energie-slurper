import os
from pathlib import Path

from data_loader import get_token, load_new_data
from database import convert_interval_to_date, float_from_string, update_row

load_new_data(get_token())

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
                    record = [key, parts[0], hour, day, month, year, float_from_string(parts[1]),
                              float_from_string(parts[2]),
                              float_from_string(parts[3]), float_from_string(parts[4]), float_from_string(parts[5])]
                    update_row(record)



