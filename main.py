import argparse

import data_loader
import graph


def handle_graph_command(start_date, end_date, aggregation):
    print(
        f'Received graph command with parameters: start_date = {start_date}, end_date = {end_date}, aggregation level = {aggregation}')
    graph.graph(start_date=start_date, end_date=end_date, aggregation_level=aggregation)


def handle_load_command(start_date, end_date):
    print(f'{start_date}, {end_date}')


def handle_update_command():
    print('Received update command, loading new data.')
    data_loader.load_new_data(data_loader.get_token())


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help='help for subcommand', dest="subcommand", required=True)

load_data_parser = subparsers.add_parser('load', help='load data from Pure Energie and store in the database')
load_data_parser.add_argument('--start_date',
                              dest='start_date',
                              type=str,
                              help='The first date of the period to retrieve data for, yyyy-MM-dd. Defaults to most recent date in database.',
                              )
load_data_parser.add_argument('--end_date',
                              dest='end_date',
                              type=str,
                              help='The last date of the period to retrieve data for (including this date), yyyy-MM-dd. Note: this date must be later than start_date. Defaults to yesterday',
                              )

print_graph_parser = subparsers.add_parser('graph', help='create a graph for a time interval')
print_graph_parser.add_argument('--start_date',
                                dest='start_date',
                                type=str,
                                help='First date of the interval to print a graph for, yyyy-MM-dd',
                                )
print_graph_parser.add_argument('--end_date',
                                dest='end_date',
                                type=str,
                                help='Last date of the interval to print a graph for (including this date), yyyy-MM-dd',
                                )
print_graph_parser.add_argument('--aggregation',
                                dest='aggregation',
                                choices=graph.AGGREGATION_LEVELS,
                                help='The aggregation level of the graph',
                                required=True
                                )

update_parameter = subparsers.add_parser('update', help='load new data')

command = parser.parse_args()
if command.subcommand == 'graph':
    handle_graph_command(command.start_date, command.end_date, command.aggregation)
elif command.subcommand == 'load':
    handle_load_command(command.start_date, command.end_date)
else:
    handle_update_command()

# functions:
# -  load new data
# - reload
# - get graph for a period
