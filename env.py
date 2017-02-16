'''
    XXXENV is a list of dicts, ordered by scopeXXX

    ENV contains a pointer to memory

    In memory, an env consists of a list:
        [ <frame>, <pointer to enclosing env> ],
    where a frame is a dictionary

    TODO:
        * figure out persisting global env
            * root pointer?
        * figure out how to write to same address
'''

from reg import fetch, assign, ENV, VAL, UNEV, ARGL
from prim import PRIMITIVES
from mem import *


UNBOUND = 'UNBOUND'


def read_env_from_memory():
    "read env from memory"
    return read_from_address(fetch(ENV))

def write_env_to_memory(env):
    "write env to memory at the earliest available address"
    address = write_to_free_address(env)
    assign(ENV, address)

def lookup(reg):
    "return the value bound to var (in reg) in current env"
    var = fetch(reg)

    if var in PRIMITIVES:
        return var

    env = read_env_from_memory()

    while env:
        frame, enclosure = env
        if var in frame:
            return frame[var]
        else:
            env = enclosure

    return UNBOUND

def define_var():
    "bind var (in UNEV) to val (in VAL) in the most recent frame"
    var, val, env = _get_var_val_env()
    frame, enclosure = env
    frame[var] = val
    write_env_to_memory([frame, enclosure])

def set_var():
    "bind the most recent occurence of var (in UNEV) to val (in VAL)"
    var, val, env = _get_var_val_env()

    while env:
        frame, enclosure = env
        if var in frame:
            frame[var] = val
            write_env_to_memory([frame, enclosure])
        else:
            env = enclosure

    # raise exception? return dummy val?

def extend_env():
    env_pointer = fetch(ENV)
    params = fetch(UNEV)
    args = fetch(ARGL)

    new_frame = dict(zip(params, args))

    ext_env = [new_frame, env_pointer]

    write_env_to_memory(ext_env)

# initialization

def initial_env():
    return [{}, None]

def initialize_env():
    env = initial_env()
    write_env_to_memory(env)

def set_global_env():
    env = fetch(ENV)
    base_frame = env[-1]
    assign(ENV, [base_frame])

# helpers

def _get_var_val_env():
    var = fetch(UNEV)
    val = fetch(VAL)
    env = read_env_from_memory()
    return var, val, env
