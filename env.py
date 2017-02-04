from reg import *

'''
ENV is a list of dicts, ordered by scope
'''

UNBOUND = 'UNBOUND'


def lookup(reg):
	"lookup the value of the contents of reg"

	var = fetch(reg)
	env = fetch(ENV)

	for frame in env:
		if var in frame:
			return frame[var]

	return UNBOUND

def defineVar():
	"bind the contents of UNEV to the contents of VAL in the newest frame"
	var, val, env = _get_var_val_env()

	try:
		env[0][var] = val
	except KeyError:
		env = {var : val}

	assign(ENV, env)

def setVar():
	var, val, env = _get_var_val_env()

	for frame in env:
		if var in frame:
			frame[var] = val
			assign(ENV, env)
			return

	# raise exception? return dummy val?

def initial_env():
	return [ {} ]

def initialize_env():
	assign(ENV, initial_env())

def _get_var_val_env():
	regs = UNEV, VAL, ENV
	return [fetch(reg) for reg in regs]
