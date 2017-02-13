'''
    TODO:
        * move INFO flag to config register
        * figure out import circularity with instr.py
'''

from reg import fetch, REGISTERS
from stack import STACK
from instr import INSTR

INFO = 1

def display_info():
    if INFO:
        show_instr()
        show_registers()
        show_stack()
        print()
        divider('*')

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
    for entry in fetch(STACK):
        print(' *', entry)

def show_instr():
    print(INSTR)
    print(fetch(INSTR))

def divider(char):
    print(char * 5)
