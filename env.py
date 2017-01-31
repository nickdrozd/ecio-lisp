from reg import *

'''
ENV consists of pair
[
	{<frame vals>},
	[<lower env / empty>]
]
'''

UNBOUND = 'UNBOUND'

def lookup(reg):
	frame, lower = fetch(ENV)
	var = fetch(reg)
	
	while frame:
		if var in frame:
			return frame[var]
		elif lower:
			frame, lower = lower
		else:
			return UNBOUND

def defineVar():
	frame, lower = fetch(ENV)
	var, val = fetch(UNEV), fetch(VAL)
	frame[var] = val
	assign(ENV, [frame, lower])

def setVar():
	frame, lower = fetch(ENV)
	var, val = fetch(UNEV), fetch(VAL)

	while frame:
		if var in frame:
			frame[var] = val
			assign(ENV, [frame, lower])
			break
		elif lower:
			frame, lower = lower
		else:
			break
			# raise exception? return dummy val

def initial_env():
	return [ {}, [] ]

def initialize_env():
	assign(ENV, initial_env())