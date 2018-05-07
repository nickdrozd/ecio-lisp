from stats import read_stats


from typing import Any
STATE = {
    'REGISTERS': {
        'VAL': None,
        'EXPR': None,
        'ENV': None,
        'FUNC': None,
        'ARGL': None,
        'CONT': None,
        'UNEV': None,
    },
    'STACK': None,
    'INSTR': None,
    'MEM': None,
}


@read_stats
def read_file(file_name, default='"?"'):
    try:
        return STATE[file_name]
    except KeyError:
        try:
            return STATE['REGISTERS'][file_name]
        except KeyError:
            return default


def write_file(file_name: str, data: Any, indent: int = 4) -> None:
    if file_name in STATE:
        STATE[file_name] = data
    elif file_name in STATE['REGISTERS']:
        STATE['REGISTERS'][file_name] = data
    else:
        raise Exception('Unknown value {}'.format(file_name))
