STACK = 'STACK'

def save(reg):
	with open(STACK, 'r+') as stack, open(reg, 'r') as regf:
		joiner = '' if stack.read() == '' else '\n'
		stack.write(joiner + regf.read())


def restore(reg):
	with open(STACK, 'r+') as stack, open(reg, 'w') as regf:
		*tail, head = stack.read().split('\n')
		# print('TAIL:', tail)
		# print('HEAD:', head)
		regf.write(head)
		tail = '\n'.join(tail)
		stack.seek(len(tail))
		stack.truncate()

def clear_stack():
	with open(STACK, 'w'):
		pass
