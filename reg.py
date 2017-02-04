import json

EXPR = 'EXPR'
VAL = 'VAL'
ENV = 'ENV'
UNEV = 'UNEV'
FUNC = 'FUNC'
ARGL = 'ARGL'
CONT = 'CONT'

REGISTERS = EXPR, VAL, ENV, UNEV, FUNC, ARGL, CONT

def fetch(reg):
	with open(reg, 'r') as regf:
		return json.loads(regf.read())

def assign(reg, val):
	with open(reg, 'w') as regf:
		regf.write(json.dumps(val))

def set_continue(label):
	assign(CONT, label)

def set_empty_arglist():
	assign(ARGL, [])

def clear_register(reg):
	with open(reg, 'w'):
		pass

def clear_registers():
	for reg in REGISTERS:
		clear_register(reg)

def show_register(reg):
	print(fetch(reg))
