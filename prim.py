'''
    TODO:
        * funcs of different arity
        * read, display, etc
'''

import operator

from reg import fetch, assign, FUNC, ARGL, VAL

PRIM_ADD = '_+'
PRIM_MUL = '_*'
PRIM_SUB = '_-'
PRIM_DIV = '_/'

PRIMITIVES = {
    PRIM_ADD : operator.add,
    PRIM_MUL : operator.mul,
    PRIM_SUB : operator.sub,
    PRIM_DIV : operator.floordiv,
}

def is_primitive_func():
    try:
        return fetch(FUNC) in PRIMITIVES
    except TypeError:
        return False

# prim funcs assumed to take two args
def apply_primitive_func():
    func = PRIMITIVES[fetch(FUNC)]
    arg1, arg2 = fetch(ARGL)

    result = func(arg1, arg2)

    assign(VAL, result)
