# register shorthand
EXPR = 'EXPR'
VAL = 'VAL'
ENV = 'ENV'
UNEV = 'UNEV'
FUNC = 'FUNC'
ARGL = 'ARGL'
CONT = 'CONT'
CURR = 'CURR'

STACK = 'STACK'

def fetch(reg):
	with open(reg, 'r') as regf:
		return regf.read()

def assign(src, dst):
	with open(src, 'r') as srcf, open(dst, 'w') as dstf:
		dstf.write(srcf.read())