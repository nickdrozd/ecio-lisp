'''
	TODO:
		* move dispatch table to labels? elsewhere?
		* figure out DONE
'''

from reg import *
from labels import *

from env import initialize_env

from evalExp import evalExp
from evalFuncs import *

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

def initialize():
	initialize_env()
	initialize_cont()
	goto_eval()

def step():
	label = fetch(INSTR)

	labels = {
		EVAL_EXP : evalExp,
		DID_DEF_VAL : did_def_val,
		IF_DECIDE : if_decide,
		IF_ELSE : if_else
	}

	try:
		next_instr = labels[label]
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
		step()
