'''
	TODO:
		* move dispatch table to labels? elsewhere?
		* figure out DONE
'''

from reg import *
from stack import clear_stack

from labels import *
from switch import switch

from info import display_info

INSTR = 'INSTR'

def goto(label):
	assign(INSTR, label)

def goto_continue():
	goto(fetch(CONT))

def goto_eval():
	goto(EVAL_EXP)

def initialize_cont():
	assign(CONT, DONE)

def initialize():
	clear_stack()
	initialize_cont()
	goto_eval()

def step():
	label = fetch(INSTR)

	try:
		next_instr = switch[label]
	except:
		raise Exception('Unknown label: {}'.format(label))

	if next_instr == DONE:
		goto_eval()
		return
	else:
		next_instr()

def done():
	return fetch(INSTR) == DONE

def run():
	initialize()
	while not done():
		display_info()
		step()
