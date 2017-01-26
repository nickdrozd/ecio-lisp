# register shorthand
EXPR = 'EXPR'
VAL = 'VAL'
ENV = 'ENV'
UNEV = 'UNEV'
FUNC = 'FUNC'
ARGL = 'ARGL'
CONT = 'CONT'

def fetch(reg):
	with open(reg, 'r') as regf:
		return regf.read()

def assign(reg, val):
	with open(reg, 'w') as regf:
		regf.write(val)

def set_continue(label):
	assign(CONT, label)