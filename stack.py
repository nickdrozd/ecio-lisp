from reg import *

def save(reg):
	with open(STACK, 'a') as stackf:
		with open(reg, 'r') as regf:
			stackf.write(str(regf.read()) + '\n')

def restore(reg):
	with open(STACK, 'r+') as stackf:
		with open(reg, 'w') as regf:
			*tail, head = stackf.read().split('\n')
			regf.write(head)
			tail = '\n'.join(tail)
			stackf.seek(len(tail))
			stackf.truncate()