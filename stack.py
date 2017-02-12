'''
The stack is conceptually distinct from the
registers, but in terms of file I/O, it will
work the same, so it will be implemented
using basic register operations.
'''

from reg import fetch, assign

STACK = 'STACK'

def save(reg):
	reg_contents = fetch(reg)
	stack = fetch(STACK)
	join = [reg_contents] + stack
	assign(STACK, join)

def restore(reg):
	top, *rest = fetch(STACK)
	assign(reg, top)
	assign(STACK, rest)

def clear_stack():
	assign(STACK, [])
