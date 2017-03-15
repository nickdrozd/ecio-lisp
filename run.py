from env import load_global_env
from garbage import collect_garbage_if_needed

import ec_main

from instr import curr_instr, set_continue, goto, DONE

from info import display_info

from stats import run_stats


def initialize_cont():
    set_continue(DONE)

def initialize_run():
    collect_garbage_if_needed()
    load_global_env()
    initialize_cont()
    _goto_eval()

def step():
    label = curr_instr()

    try:
        next_instr = getattr(ec_main, label)
        next_instr()
    except:
        raise Exception('Unknown label: {}'.format(label))

    # input()

@run_stats
def run(info_flag=0):
    initialize_run()

    while curr_instr() != DONE:
        display_info(info_flag)
        step()

def _goto_eval():
    goto(ec_main.EVAL_EXPR)
