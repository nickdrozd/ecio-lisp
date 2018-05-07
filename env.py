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
from lib import LIBRARY, MACRO
from prim import is_primitive
from mem import ROOT, read_from_address, write_to_address, write_to_free_address


from typing import Any, Dict, List, Optional, Union
UNBOUND = 'UNBOUND'


def read_env_from_memory() -> Any:
    "read env from memory"
    address = fetch(ENV)
    return read_from_address(address), address


def write_env_to_new_memory(env: Union[List[Union[Dict[str, int], str]], List[Union[Dict[str, Union[int, List[int]]], str]], List[Union[Dict[str, Union[str, int, List[int]]], str]], List[Union[Dict[str, List[Any]], str]], List[Union[Dict[str, List[int]], str]]]) -> None:
    "write env to memory at the earliest available address"
    address = write_to_free_address(env)
    assign(ENV, address)


def lookup_expr() -> Any:
    "return the value bound to var (in EXPR) in current env"
    var = fetch(EXPR)

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


def is_unbound(reg: str) -> bool:
    return fetch(reg) == UNBOUND


def define_var() -> None:
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


def is_macro(expr: Union[List[Union[str, List[Union[str, List[str]]], List[str]]], List[Union[List[Union[str, List[Union[str, List[str]]], List[str]]], str]], str]) -> bool:
    global_frame, _ = read_from_address(ROOT)
    return expr in global_frame[MACRO]


def extend_env() -> None:
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

def initial_env() -> List[Union[Dict[str, Union[List[Union[str, List[List[Union[str, int]]]]], str, List[Union[str, List[str], List[List[Union[str, int]]]]], List[Union[str, List[str], List[Union[List[Union[str, List[Union[str, List[str], List[Union[str, List[str], List[Union[str, List[Union[str, List[str]]], List[str]]]]]]]]], List[str]]]]], List[Union[str, List[str]]], List[Union[str, List[str], List[List[Union[str, List[str]]]]]], List[Union[str, List[str], List[List[str]]]]]], NoneType]]:
    return [LIBRARY, None]


def initialize_env() -> None:
    write_to_address(initial_env(), ROOT)


def load_global_env() -> None:
    assign(ENV, ROOT)
