import argparse
from data_loader import get_token, get_data_for_period
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('--start_date', dest='start_date', type=str,
                    help='The first date of the period to retrieve data for, yyyy-MM-dd',
                    required=True)
parser.add_argument('--end_date', dest='end_date', type=str,
                    help='The last date of the period to retrieve data for, yyyy-MM-dd. Note: this date must be later than start_date',
                    required=True)
args = parser.parse_args()

token = get_token()

start_date =  datetime.strptime(args.start_date, '%Y-%m-%d').date()
end_date =  datetime.strptime(args.end_date, '%Y-%m-%d').date()
data = get_data_for_period(start_date, end_date, token)
print(data)
