from reg import *

INSTR = 'INSTR'

def goto(label):
	assign(INSTR, label)

def goto_continue():
	goto(fetch(CONT))

def goto_eval():
	goto('EVAL_EXP')

def execute():
	labels = {
		'EVAL_EXP': evalExp
	}

	label = fetch(INSTR)

	try:
		label()
	except:
		raise Exception('Unknown label: {}'.format(label))