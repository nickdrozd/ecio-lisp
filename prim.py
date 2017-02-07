'''
	TODO:
		* funcs of different arity
		* read, display, etc
'''

import operator

from reg import *

prim_add = '_+'
prim_mul = '_*'
prim_sub = '_-'
prim_div = '_/'

primitives = {
	prim_add : operator.add,
	prim_mul : operator.mul,
	prim_sub : operator.sub,
	prim_div : operator.floordiv,
}

def is_primitive_func():
	try:
		return fetch(FUNC) in primitives
	except:
		return False

# prim funcs assumed to take two args
def apply_primitive_func():
	func = primitives[fetch(FUNC)]
	arg1, arg2 = fetch(ARGL)

	result = func(arg1, arg2)

	assign(VAL, func(arg1, arg2))
