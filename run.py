from reg import *
from stack import clear_stack
from env import initialize_env
from instr import *
from parse import parse
from evalExp import evalExp

def get_expr():
	expr = parse(input())
	assign(EXPR, expr)


def initialize():
	clear_registers()
	clear_stack()

	initialize_env()
	initialize_cont()


def run():
	initialize()
	get_expr()
	evalExp()


def step():
	"don't run the whole thing, just one step"

