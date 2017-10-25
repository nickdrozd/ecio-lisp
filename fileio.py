import json

from stats import read_stats


@read_stats
def read_file(file_name, default='"?"'):
    try:
        file = open(file_name, 'r')
    except FileNotFoundError:
        print('Creating file {}'.format(file_name))
        file = open(file_name, 'w+')
        file.write(default)

    contents = json.loads(file.read())

    file.close()

    return contents


def write_file(file_name, data, indent=4):
    with open(file_name, 'w+') as file:
        file.write(
            json.dumps(
                data,
                sort_keys=True,
                indent=indent))
