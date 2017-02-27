'''
    TODO:
        * figure out a better way to resolve circular imports
'''

from reg import fetch, assign, CONT # clear_registers?

# initialize_run
from env import load_global_env
from garbage import collect_garbage_if_needed

from switch import switch
from labels import DONE, EVAL_EXP

from stats import goto_stats
from stats import run_stats

INSTR = 'INSTR'

# info.py imports INSTR
from info import display_info

@goto_stats
def goto(label):
    assign(INSTR, label)

def goto_continue():
    goto(fetch(CONT))

def goto_eval():
    goto(EVAL_EXP)

def set_continue(label):
    assign(CONT, label)

def initialize_cont():
    set_continue(DONE)

def initialize_run():
    collect_garbage_if_needed()
    load_global_env()
    initialize_cont()
    goto_eval()

def step():
    label = fetch(INSTR)

    try:
        next_instr = switch[label]
    except:
        raise Exception('Unknown label: {}'.format(label))

    if next_instr == DONE:
        goto_eval()
        return
    else:
        next_instr()

def done():
    return fetch(INSTR) == DONE

@run_stats
def run(info_flag=0):
    initialize_run()

    while not done():
        display_info(info_flag)
        step()
