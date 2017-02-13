from reg import fetch, assign, EXPR, VAL
from env import initialize_env
from instr import run
from parse import parse

INTERPRETER_PROMPT = '<<< '
INTERPRETER_EXIT = '.quit', '.exit'
EXIT_MESSAGE = 'Byeeeeeeee!'

def repl():
    while True:
        initialize_env() # should be load_global_env
        try:
            get_expr()
            run()
            print_result()
        except KeyboardInterrupt:
            print()
            break
        # except Exception as e: # better way to do this?
        #   print(e)
        #   break

def get_expr():
    expr = parse(input(INTERPRETER_PROMPT))

    if expr in INTERPRETER_EXIT:
        raise Exception(EXIT_MESSAGE)
    else:
        assign(EXPR, expr)

def print_result():
    print(fetch(VAL))

if __name__ == '__main__':
    repl()
