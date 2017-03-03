'''
    TODO:
        * funcs of different arity
        * read, display, etc
'''

import operator
from parse import parse

from reg import fetch, assign, FUNC, ARGL, VAL

# primitive i/o

ARITY_0 = {
    'read' : lambda: parse(input()),
}

ARITY_1 = {
    'show' : print,
}

ARITY_2 = {
    # primitive arithmetic

    '_+' : operator.add,
    '_*' : operator.mul,
    '_-' : operator.sub,
    '_/' : operator.floordiv,

    '=' : operator.eq,
    '<' : operator.lt,
    '>' : operator.gt,
}

def is_primitive(var):
    try:
        return any(
            var in primitives for primitives in
            [ARITY_0, ARITY_1, ARITY_2]
        )
    except TypeError:
        return False
    
def is_primitive_func():
    return is_primitive(fetch(FUNC))

# prim funcs assumed to take two args
def apply_primitive_func():
    func = fetch(FUNC)

    if func in ARITY_0:
        prim = ARITY_0[func]
        result = prim()

    if func in ARITY_1:
        prim = ARITY_1[func]
        arg1, = fetch(ARGL)
        result = prim(arg1)

    if func in ARITY_2:
        prim = ARITY_2[func]
        arg1, arg2 = fetch(ARGL)
        result = prim(arg1, arg2)

    assign(VAL, result)
