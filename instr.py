'''
	TODO:
		* move dispatch table to labels? elsewhere?
		* figure out DONE
'''

from reg import *
from labels import *
from stack import clear_stack

from evalExp import evalExp
from evalFuncs import *

from info import display_info

INSTR = 'INSTR'
DONE = 'DONE'

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

	labels = {
		EVAL_EXP : evalExp,

		DID_DEF_VAL : did_def_val,

		IF_DECIDE : if_decide,
		IF_THEN : if_then,
		IF_ELSE : if_else,

		DID_FUNC : did_func,
		CHECK_NO_ARGS : check_no_args,
		LAST_ARG : last_arg,
		ARG_LOOP : arg_loop,
		ACC_ARG : acc_arg,

		APPLY_FUNC : applyFunc,

		APPLY_PRIMITIVE : apply_primitive,
		APPLY_COMPOUND : apply_compound,

		EVAL_SEQ : eval_seq,
		EVAL_SEQ_CONT : eval_seq_cont,
		EVAL_SEQ_LAST : eval_seq_last,

		ALT_EVAL_SEQ : alt_eval_seq,
		ALT_EVAL_SEQ_END : alt_eval_seq_end,
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
		display_info()
		step()
