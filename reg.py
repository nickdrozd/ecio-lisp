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

def assign(dst, val):
	with open(src, 'r') as dstf:
		dstf.write(val)
