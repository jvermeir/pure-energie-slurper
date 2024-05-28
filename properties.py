import json
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
