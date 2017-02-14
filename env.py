'''
    ENV is a list of dicts, ordered by scope

    TODO:
        * figure out persisting global env
            * add memory section?
                * naming? gensym?
'''

from reg import fetch, assign, ENV, VAL, UNEV, ARGL
from prim import PRIMITIVES


UNBOUND = 'UNBOUND'


def lookup(reg):
    "lookup the value of the contents of reg"

    var = fetch(reg)

    if var in PRIMITIVES:
        return var

    env = fetch(ENV)

    for frame in env:
        if var in frame:
            return frame[var]

    return UNBOUND

def define_var():
    "bind the contents of UNEV to the contents of VAL in the newest frame"
    var, val, env = _get_var_val_env()

    try:
        env[0][var] = val
    except KeyError:
        env = {var : val}

    assign(ENV, env)

def set_var():
    var, val, env = _get_var_val_env()

    for frame in env:
        if var in frame:
            frame[var] = val
            assign(ENV, env)
            return

    # raise exception? return dummy val?

def extend_env():
    env = fetch(ENV)
    params = fetch(UNEV)
    args = fetch(ARGL)

    new_frame = dict(zip(params, args))

    ext_env = [new_frame] + env

    assign(ENV, ext_env)

def initial_env():
    return [{}]

def initialize_env():
    assign(ENV, initial_env())

def set_global_env():
    env = fetch(ENV)
    base_frame = env[-1]
    assign(ENV, [base_frame])    

def _get_var_val_env():
    regs = UNEV, VAL, ENV
    return [fetch(reg) for reg in regs]
