'''
    TODO:
        * syntax checking (paren count, etc)
            * in parse or in get_expr?
'''

from reg import fetch, assign, EXPR, VAL
from env import initialize_env, load_global_env
from instr import run
from parse import parse
from stats import display_stats
from garbage import collect_garbage_if_needed

INTERPRETER_PROMPT = '<<< '
INTERPRETER_EXIT = '.quit', '.exit'
EXIT_MESSAGE = 'Byeeeeeeee!'

def repl():
    initialize_env()
    while True:
        collect_garbage_if_needed()
        load_global_env()
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
    expr = parse(input(INTERPRETER_PROMPT))

    if expr in INTERPRETER_EXIT:
        raise Exception(EXIT_MESSAGE)
    else:
        assign(EXPR, expr)

def display_result():
    print(fetch(VAL))
    print()
    display_stats()
    print()


if __name__ == '__main__':
    repl()
