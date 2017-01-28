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
		return regf.read()

def assign(reg, val):
	with open(reg, 'w') as regf:
		# str(val)? json.dumps(val)?
		regf.write(val)

def set_continue(label):
	assign(CONT, label)

def clear_register(reg):
	with open(reg, 'w'):
		pass

def clear_registers():
	for reg in REGISTERS:
		clear_register(reg)
