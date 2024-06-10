import json
from datetime import timedelta, datetime
from pathlib import Path

properties_file = Path.home() / Path("pesConfig.json")

with open(properties_file, 'r') as file:
    properties_as_text = file.readline()
    config = json.loads(properties_as_text)

email = config['email']
password = config['password']
connection_id = config['connection_id']
access_token = config['access_token']
start_of_data = config['start_of_data']
influx_url = config['influx_url']
influx_token = config['influx_token']
influx_org = config['influx_org']
influx_bucket = config['influx_bucket']

INTERVAL_LENGTH_IN_DAYS = 14
DATA_ROOT_FOLDER = './data/'
DATE_FORMAT = '%Y-%m-%d'
TODAY = datetime.now().date()
YESTERDAY = TODAY - timedelta(days=1)
