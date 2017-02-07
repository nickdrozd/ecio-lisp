'''
	TODO:
		* figure out import mess
'''

from reg import *
from stack import *
from env import *
# from instr import instr.goto, instr.goto_continue, instr.goto_eval
import instr
from labels import *
from prim import *

###

def eval_num():
	assign(VAL, fetch(EXPR))
	instr.goto_continue()

def eval_var():
	assign(VAL, lookup(EXPR))
	instr.goto_continue()

def eval_quote():
	_, text = fetch(EXPR)
	assign(VAL, text)
	instr.goto_continue()

###

def eval_lambda():
	_, params, *body = fetch(EXPR)
	assign(UNEV, params)
	assign(EXPR, body)
	assign(VAL, [fetch(UNEV), fetch(EXPR), fetch(ENV)])
	instr.goto_continue()

###

def eval_def():
	_, var, val = fetch(EXPR)
	assign(UNEV, var)
	assign(EXPR, val)
	save(UNEV)
	save(ENV)
	save(CONT)
	set_continue(DID_DEF_VAL)
	instr.goto_eval()

def did_def_val():
	restore(CONT)
	restore(ENV)
	restore(UNEV)
	defineVar()
	instr.goto_continue()

###

def eval_if():
	save(ENV)
	save(CONT)
	save(EXPR)
	_, ifTest, _, _ = fetch(EXPR)
	assign(EXPR, ifTest)
	set_continue(IF_DECIDE)
	instr.goto_eval()

def if_decide():
	restore(EXPR)
	restore(CONT)
	restore(ENV)
	if fetch(VAL): # or if isTrue(fetch(VAL))
		instr.goto(IF_THEN)
	else:
		instr.goto(IF_ELSE)

def if_then():
	_, _, ifThen, _ = fetch(EXPR)
	assign(EXPR, ifThen)
	instr.goto_eval()	

def if_else():
	_, _, _, ifElse = fetch(EXPR)
	assign(EXPR, ifElse)
	instr.goto_eval()

###

def eval_func():
	save(CONT)
	save(ENV)

	func, *args = fetch(EXPR)
	assign(EXPR, func)
	assign(UNEV, args)

	save(UNEV)

	set_continue(DID_FUNC)
	instr.goto_eval()

def did_func():
	restore(UNEV) # args
	restore(ENV)

	assign(FUNC, fetch(VAL))
	set_empty_arglist()

	# cont is still/already saved
	instr.goto(CHECK_NO_ARGS)

def check_no_args():
	if not fetch(UNEV): # if no_args():
		instr.goto(APPLY_FUNC)
		return

	# if noCompoundArgs(): ...
	save(FUNC)
	instr.goto(ARG_LOOP)

def arg_loop():
	save(ARGL)

	first, *rest = fetch(UNEV)

	assign(EXPR, first)

	if not rest: # if no_remaining_args():
		set_continue(LAST_ARG)
		instr.goto_eval()
		return

	assign(UNEV, rest)

	save(ENV)
	save(UNEV)

	set_continue(ACC_ARG)
	instr.goto_eval()

def acc_arg():
	restore(UNEV)
	restore(ENV)

	restore(ARGL)

	args = fetch(ARGL) + [fetch(VAL)]
	assign(ARGL, args)

	instr.goto(ARG_LOOP)

def last_arg():
	set_continue(DID_LAST_ARG)
	instr.goto_eval()

def did_last_arg():
	restore(ARGL)

	args = fetch(ARGL) + [fetch(VAL)]
	assign(ARGL, args)

	restore(FUNC)

	instr.goto(APPLY_FUNC)

###

def apply_func():
	if is_primitive_func():
		instr.goto(APPLY_PRIMITIVE)
	# if is_compound_func():
	else:
		instr.goto(APPLY_COMPOUND)

def apply_primitive():
	apply_primitive_func()

	restore(CONT)

	instr.goto_continue()

def apply_compound():
	# this needs to agree with eval_lambda
	params, body, env = fetch(FUNC)

	assign(UNEV, params)
	assign(ENV, env)
	extend_env()

	assign(UNEV, body)

	instr.goto(EVAL_SEQ)

###

def eval_seq():
	first, *rest = fetch(UNEV)

	assign(EXPR, first)

	# if last_exp...
	if not rest:
		instr.goto(EVAL_SEQ_LAST)
		return

	assign(UNEV, rest)

	save(UNEV)
	save(ENV)

	set_continue(EVAL_SEQ_CONT)

	instr.goto_eval()

def eval_seq_cont():
	restore(ENV)
	restore(UNEV)

	instr.goto(EVAL_SEQ)

def eval_seq_last():
	restore(CONT)

	instr.goto_eval()

###

def alt_eval_seq():
	exps = fetch(UNEV)

	# if no_exps...
	if not exps:
		instr.goto(EVAL_SEQ_END)
		return

	first, *rest = fetch(UNEV)

	assign(EXPR, first)
	assign(UNEV, rest)

	save(UNEV)
	save(ENV)

	set_continue(EVAL_SEQ_CONT)

	instr.goto_eval()

def alt_eval_seq_end():
	restore(CONT)
	instr.goto_continue()









