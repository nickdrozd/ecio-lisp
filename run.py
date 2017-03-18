from env import load_global_env
from garbage import collect_garbage_if_needed

from switch import SWITCH
from labels import DONE

from instr import curr_instr, set_continue, goto_eval

from info import display_info

from stats import run_stats


def initialize_cont():
    set_continue(DONE)

def initialize_run():
    collect_garbage_if_needed()
    load_global_env()
    initialize_cont()
    goto_eval()

def done():
    return curr_instr() == DONE

def step():
    label = curr_instr()

    try:
        next_instr = SWITCH[label]
    except:
        raise Exception('Unknown label: {}'.format(label))

    if next_instr == DONE:
        goto_eval()
        return
    else:
        next_instr()

@run_stats
def run(info_flag=0):
    initialize_run()

    while not done():
        display_info(info_flag)
        step()
