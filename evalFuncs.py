# TODO:
# 	* do all saves / restores in one instr? eg save(ENV, CONT)

from reg import *
from stack import *
from env import *
from instr import *

def evalNum():
	assign(VAL, fetch(EXPR))
	goto_continue()

def evalVar():
	assign(VAL, lookup(EXPR))
	goto_continue()

def evalQuote():
	_, text = fetch(EXPR)
	assign(VAL, text)
	goto_continue()

def evalDef():
	_, var, val = fetch(EXPR)
	assign(UNEV, var)
	assign(EXPR, val)
	save(UNEV)
	save(ENV)
	save(CONT)
	set_continue('did_def_val')
	goto_eval()

def did_def_val():
	restore(CONT)
	restore(ENV)
	restore(UNEV)
	defineVar()
	goto_continue()

def evalIf():
	save(ENV)
	save(CONT)
	save(EXPR)
	_, ifTest, _, _ = fetch(EXPR)
	assign(EXPR, ifTest)
	set_continue('if_decide')
	goto_eval()

def if_decide():
	restore(EXPR)
	restore(CONT)
	restore(ENV)
	if fetch(VAL): # or if isTrue(fetch(VAL))
		goto('if_then')
	else:
		goto('if_else')

def if_then():
	_, _, ifThen, _ = fetch(EXPR)
	assign(EXPR, ifThen)
	goto_eval()	

def if_else():
	_, _, _, ifElse = fetch(EXPR)
	assign(EXPR, ifElse)
	goto_eval()
























