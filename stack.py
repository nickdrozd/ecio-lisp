STACK = 'STACK'


def save(reg):
	with open(STACK, 'r+') as stackf:
		with open(reg, 'r') as regf:
			reg_contents = str(regf.read())
			stack_contents = str(stackf.read())
			joiner = '' if stack_contents == '' else '\n'
			stackf.write(joiner + reg_contents)

def restore(reg):
	with open(STACK, 'r+') as stackf:
		with open(reg, 'w') as regf:
			*tail, head = stackf.read().split('\n')
			tail = '\n'.join(tail)
			regf.write(head)
			stackf.seek(len(tail))
			stackf.truncate()

def clear_stack():
	with open(STACK, 'w'):
		pass
