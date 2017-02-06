import json

from reg import fetch, REGISTERS
from stack import STACK
import instr

def show_register(reg):
	print(reg)
	print(fetch(reg))

def show_registers():
	for reg in REGISTERS:
		show_register(reg)
	print()

def show_stack():
	with open(STACK, 'r') as stack:
		items = stack.readlines()
		print(STACK)
		print(items)

def show_instr():
	print(instr.INSTR)
	print(fetch(instr.INSTR))
	print()

def display_info():
	show_instr()
	show_registers()
	show_stack()
	print('\n***\n')