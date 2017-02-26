'''
    TODO:
        * syntax checking (paren count, etc)
            * in parse or in get_expr?
'''

from reg import fetch, assign, EXPR, VAL
from env import initialize_env
from instr import run
from parse import parse
from stats import display_stats

INTERPRETER_PROMPT = '<<< '
INTERPRETER_EXIT = '.quit', '.exit'
EXIT_MESSAGE = 'Byeeeeeeee!'

def repl():
    initialize_env()
    while True:
        try:
            get_expr()
            run()
            display_result()
        except KeyboardInterrupt:
            print()
            break
        # except Exception as e: # better way to do this?
        #   print(e)

def get_expr():
    expr = input(INTERPRETER_PROMPT)

    if expr in INTERPRETER_EXIT:
        raise Exception(EXIT_MESSAGE)
    else:
        parse_and_set_expr(expr)

def display_result():
    print(get_result())
    print()
    display_stats()
    print()

def parse_and_set_expr(lisp_expr):
    parsed = parse(lisp_expr)
    assign(EXPR, parsed)

def get_result():
    return fetch(VAL)

if __name__ == '__main__':
    repl()
