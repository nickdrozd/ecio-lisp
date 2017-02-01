from reg import *
from stack import clear_stack
from env import initialize_env
from instr import *
from parse import parse
from evalExp import evalExp

INTERPRETER_PROMPT = '<<< '
INTERPRETER_EXIT = '.quit'

def get_expr():
	expr = parse(input(INTERPRETER_PROMPT))

	if expr == INTERPRETER_EXIT:
		raise Exception
	else:
		assign(EXPR, expr)


def get_result():
	return fetch(VAL)


def initialize():
	# clear_registers()
	# clear_stack()

	initialize_env()
	initialize_cont()


def run():
	initialize()
	get_expr()

	# while INSTR != DONE:
	# 	execute()

	evalExp() # temporary


def repl():
	while True:
		try:
			run()
			print(get_result())
		except KeyboardInterrupt:
			print()
			break
		except:
			break


def step():
	"don't run the whole thing, just one step"

if __name__ == '__main__':
	repl()