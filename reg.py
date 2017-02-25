import json

EXPR = 'EXPR'
VAL = 'VAL'
ENV = 'ENV'
UNEV = 'UNEV'
FUNC = 'FUNC'
ARGL = 'ARGL'
CONT = 'CONT'

REGISTERS = EXPR, VAL, ENV, UNEV, FUNC, ARGL, CONT

EMPTY_REG = '"***"'

# basic register operations

def fetch(reg):
    with open(reg, 'r') as regf:
        return json.loads(regf.read())

def assign(reg, val):
    with open(reg, 'w') as regf:
        regf.write(json.dumps(val, sort_keys=True, indent=4))

def clear_register(reg):
    with open(reg, 'w') as regf:
        regf.write(EMPTY_REG)

def clear_registers():
    for reg in REGISTERS:
        clear_register(reg)

# particular register operations

def set_continue(label):
    assign(CONT, label)

def set_empty_arglist():
    assign(ARGL, [])

def adjoin_arg():
    curr_args = fetch(ARGL)
    new_arg = fetch(VAL)
    adjoined = curr_args + [new_arg]
    assign(ARGL, adjoined)
