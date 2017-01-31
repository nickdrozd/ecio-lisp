from init import initialize
from evalExp import evalExp

def run():
	expr = get_expr() # TODO
	initialize(expr)
	evalExp()


def step():
	"don't run the whole thing, just one step"

