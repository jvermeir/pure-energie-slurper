import os
from pathlib import Path

import influx
from database import update_data


def load_datafiles():
    data_folder = Path(__file__).with_name('data').absolute()
    files = list(filter(lambda file: file.endswith('.csv'), sorted(os.listdir(data_folder))))
    for file in files:
        print(file)
        absolute_file = os.path.join(data_folder, file)
        with open(absolute_file, 'r') as data_file:
            data = data_file.read()
            update_data(data)
            influx.update_data(data)


# load_new_data(get_token())
load_datafiles()