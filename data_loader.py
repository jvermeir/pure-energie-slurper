import json
import os
from datetime import datetime, timedelta

import requests

import properties

INTERVAL_LENGTH_IN_DAYS = 14
DATA_ROOT_FOLDER = './data/'
DATE_FORMAT = '%Y-%m-%d'
TODAY = datetime.now().date()
YESTERDAY = TODAY - timedelta(days=1)


def get_token():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Content-Type': 'application/json',
        'Referer': 'https://pure-energie.nl/',
        'Origin': 'https://pure-energie.nl',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'DNT': '1',
        'Sec-GPC': '1',
        'Connection': 'keep-alive',
        'Priority': 'u=1',
        'TE': 'trailers'
    }
    credentials = json.dumps({"email": properties.email, "password": properties.password})
    login_response = requests.post('https://dmp.pure-energie.nl/api/auth/login', data=credentials,
                                   headers=headers)

    data = login_response.json()
    return data['access_token']


def get_data_for_period(start_date, end_date, token):
    get_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Referer': 'https://pure-energie.nl/',
        'X-Token': properties.access_token,
        'Origin': 'https://pure-energie.nl',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'DNT': '1',
        'Sec-GPC': '1',
        'authorization': f'Bearer {token}',
        'Connection': 'keep-alive',
        'TE': 'trailers'
    }

    response = requests.get(
        f'https://dmp.pure-energie.nl/api/klantportaal/{properties.connection_id}/consumption/download?period=hours&start_date={start_date}&end_date={end_date}',
        headers=get_headers)
    return json.loads(response.text)['content']


def write_data_to_file(start_date, data):
    date = start_date.strftime(DATE_FORMAT)
    with open(DATA_ROOT_FOLDER + date + '.csv', 'w') as data_file:
        data_file.write(data)


def find_latest_data_file_name():
    files = list(filter(lambda file: file.endswith('.csv'), sorted(os.listdir(DATA_ROOT_FOLDER))))
    if len(files) == 0:
        return datetime(2016, 11, 19).strftime(DATE_FORMAT) + '.csv'
    return files[-1]


def find_end_date(the_date):
    end_date = the_date + timedelta(days=14)
    if end_date >= TODAY:
        return YESTERDAY
    return end_date


def should_continue(interval_end_date, most_recent_available_date):
    return interval_end_date <= most_recent_available_date


def load_new_data(token):
    latest_file_name = find_latest_data_file_name()
    the_date = datetime.strptime(latest_file_name.replace('.csv', ''), DATE_FORMAT).date()

    while should_continue(the_date, YESTERDAY):
        print(the_date)
        end_date = find_end_date(the_date)
        data = get_data_for_period(the_date, end_date, token)
        write_data_to_file(the_date, data)
        the_date = the_date + timedelta(days=INTERVAL_LENGTH_IN_DAYS)
