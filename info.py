'''
    TODO:
        * better formatting
'''

from reg import fetch, REGISTERS
from stack import STACK, read_stack
from instr import INSTR


def display_info(info_flag: int = 0) -> None:
    if info_flag:
        show_instr()
        show_registers()
        show_stack()
        print()
        divider('*', 3)


def show_register(reg):
    divider('-')
    print(reg)
    print(fetch(reg))


def show_registers():
    for reg in REGISTERS:
        show_register(reg)
    divider('-')


def show_stack():
    print(STACK)
    for entry in read_stack():
        print(' *', entry)
    divider('*', 3)
    print('\n\n')


def show_instr():
    print(INSTR)
    print(fetch(INSTR))


def divider(char, length=1):
    print(char * (5 * length))
