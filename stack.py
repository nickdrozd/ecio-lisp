from reg import *

STACK = 'STACK'

def save(reg):
	with open(STACK, 'r+') as stack:
		joiner = '' if stack.read() == '' else '\n'
		stack.write(joiner + fetch(reg))

def restore(reg):
	with open(STACK, 'r+') as stack:
		*tail, head = stack.read().split('\n')
		assign(reg, head)
		tail = '\n'.join(tail)
		stack.seek(len(tail))
		stack.truncate()

def clear_stack():
	with open(STACK, 'w'):
		pass
