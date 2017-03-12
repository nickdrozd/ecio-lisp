'''
    XXXENV is a list of dicts, ordered by scopeXXX

    ENV contains a pointer to memory

    In memory, an env consists of a list:
        [ <frame>, <pointer to enclosing env> ],
    where a frame is a dictionary

    TODO:
        * clean up mem imports
            * consolidate read/write functions?
            * should read_from_address return env, address pair?
        * figure out define / defmacro interactions
'''

from reg import fetch, assign, EXPR, ENV, VAL, UNEV, ARGL
from labels import UNBOUND
from lib import LIBRARY, MACRO
from prim import is_primitive
from mem import ROOT, read_from_address, write_to_address, write_to_free_address


def read_env_from_memory():
    "read env from memory"
    address = fetch(ENV)
    return read_from_address(address), address

def write_env_to_new_memory(env):
    "write env to memory at the earliest available address"
    address = write_to_free_address(env)
    assign(ENV, address)

def lookup(reg):
    "return the value bound to var (in reg) in current env"
    var = fetch(reg)

    if is_primitive(var):
        return var

    env, _ = read_env_from_memory()

    while env:
        frame, enclosure = env
        if var in frame:
            return frame[var]
        else:
            env = read_from_address(enclosure) if enclosure else None

    return UNBOUND

def is_unbound(reg):
    return fetch(reg) == UNBOUND

def define_var():
    "bind var (in UNEV) to val (in VAL) in the most recent frame"
    var, val = fetch(UNEV), fetch(VAL)
    env, address = read_env_from_memory()
    frame, enclosure = env
    frame[var] = val
    write_to_address([frame, enclosure], address)

def set_var():
    "bind the most recent occurence of var (in UNEV) to val (in VAL)"
    var, val = fetch(UNEV), fetch(VAL)

    env, address = read_env_from_memory()

    while env:
        frame, enclosure = env
        if var in frame:
            frame[var] = val
            updated_env = [frame, enclosure]
            write_to_address(updated_env, address)
            return
        else:
            env, address = read_from_address(enclosure), enclosure

    # raise exception? return dummy val?

def define_macro():
    _, macro_name, params, expr = fetch(EXPR)

    macro_def = [MACRO, params, expr]

    # all macros are assigned to global env
    global_frame, enclosure = read_from_address(ROOT)

    # add macro name to macro list
    global_frame[MACRO].append(macro_name)

    # install macro
    global_frame[macro_name] = macro_def

    write_to_address([global_frame, enclosure], ROOT)

def is_macro(expr):
    global_frame, _ = read_from_address(ROOT)
    return expr in global_frame[MACRO]

def extend_env():
    env_pointer = fetch(ENV)
    params = fetch(UNEV)
    args = fetch(ARGL)

    if isinstance(params, str):
        new_frame = dict(zip([params], [args]))
    else:
        new_frame = dict(zip(params, args))

    ext_env = [new_frame, env_pointer]

    write_env_to_new_memory(ext_env)

# initialization

def initial_env():
    return [LIBRARY, None]

def initialize_env():
    write_to_address(initial_env(), ROOT)

def load_global_env():
    assign(ENV, ROOT)
