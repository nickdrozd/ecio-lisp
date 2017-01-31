from reg import *

INSTR = 'INSTR'
DONE = 'done'

def goto(label):
	assign(INSTR, label)

def goto_continue():
	goto(fetch(CONT))

def goto_eval():
	goto(EVAL_EXP)

def initialize_cont():
	assign(CONT, DONE)

def execute():
	labels = {
		EVAL_EXP: evalExp
	}

	label = fetch(INSTR)

	try:
		label()
	except:
		raise Exception('Unknown label: {}'.format(label))

# labels (separate file?)

EVAL_EXP = 'EVAL_EXP'
