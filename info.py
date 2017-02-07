'''
	TODO:
		* move INFO flag to config register
'''

import json

from reg import fetch, REGISTERS
from stack import STACK
import instr

INFO = 0

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
	with open(STACK, 'r') as stack:
		items = stack.readlines()
		print(STACK)
		print(items)

def show_instr():
	print(instr.INSTR)
	print(fetch(instr.INSTR))

def divider(char):
	print(char * 5)
