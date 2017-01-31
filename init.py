from reg import EXPR, assign

from reg import clear_registers
from stack import clear_stack
from env import initialize_env
from instr import initialize_cont

def initialize(expr):
	clear_registers()
	clear_stack()

	initialize_env()
	initialize_cont()

	assign(EXPR, expr)