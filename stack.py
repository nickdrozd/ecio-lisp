import fileio
from reg import fetch, assign
from stats import save_stats, restore_stats

STACK = 'STACK'

EMPTY_STACK = []


def read_stack():
    return fileio.read_file(STACK, default=EMPTY_STACK)


def write_stack(data):
    fileio.write_file(STACK, data)


@save_stats
def save(reg):
    reg_contents = fetch(reg)
    stack = read_stack()
    join = [reg_contents] + stack
    write_stack(join)


@restore_stats
def restore(reg):
    top, *rest = fetch(STACK)
    assign(reg, top)
    write_stack(rest)


def clear_stack():
    write_stack(EMPTY_STACK)
