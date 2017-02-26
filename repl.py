'''
    TODO:
        * syntax checking (paren count, etc)
            * in parse or in get_expr?
        * argparse, argv, cli for flags?
'''

from reg import fetch, assign, EXPR, VAL, clear_registers
from stack import clear_stack
from mem import clear_memory
from env import initialize_env
from instr import run
from parse import parse
from stats import display_stats

INTERPRETER_PROMPT = '<<< '
INTERPRETER_EXIT = '.quit', '.exit'
EXIT_MESSAGE = 'Byeeeeeeee!'

def repl():
    info_flag = 0
    stats_flag = 1

    initialize()
    while True:
        try:
            get_expr()
            run(info_flag=info_flag)
            display_result(stats_flag=stats_flag)
        except KeyboardInterrupt:
            print()
            break
        # except Exception as e: # better way to do this?
        #   print(e)

def ecio_eval(expr):
    '''Evaluates an expression without invoking the repl'''

    initialize()
    parse_and_set_expr(expr)
    run()
    return get_result()

def initialize():
    # optional
    clear_registers()
    clear_stack()
    clear_memory()
    # required
    initialize_env()

def get_expr():
    expr = input(INTERPRETER_PROMPT)

    if expr in INTERPRETER_EXIT:
        raise Exception(EXIT_MESSAGE)
    else:
        parse_and_set_expr(expr)

def display_result(stats_flag=1):
    print(get_result())
    print()
    display_stats(stats_flag)
    print()

def parse_and_set_expr(lisp_expr):
    parsed = parse(lisp_expr)
    assign(EXPR, parsed)

def get_result():
    return fetch(VAL)

if __name__ == '__main__':
    repl()
