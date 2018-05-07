import fileio

from reg import fetch, assign, CONT

from stats import goto_stats

from typing import Callable, Union
INSTR = 'INSTR'
NO_INSTR = '"???"'
DONE = 'DONE'


@goto_stats
def goto(label):
    fileio.write_file(INSTR, _convert_label(label))


def curr_instr() -> str:
    return fileio.read_file(INSTR, NO_INSTR)


# these aren't strictly necessary, but they're very convenient.
# conceptually, we can imagine that the CONT register has some
# specialized physical connection to INSTR register
# (or PC, or whatever it really is)

def goto_continue() -> None:
    goto(fetch(CONT))


def set_continue(label: Union[str, Callable]) -> None:
    assign(CONT, _convert_label(label))


def _convert_label(label: Union[str, Callable]) -> str:
    try:
        return label.__name__
    except AttributeError:
        return label
