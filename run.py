from env import load_global_env
from garbage import collect_garbage_if_needed

from eval_exp import eval_exp
import ec_main

from instr import curr_instr, set_continue, goto_eval

from info import display_info

from stats import run_stats


DONE = 'DONE'

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

    if label == DONE:
        goto_eval()
    elif label == 'EVAL_EXP':
        eval_exp()
    else:
        try:
            next_instr = getattr(ec_main, label)
        except:
            raise Exception('Unknown label: {}'.format(label))

        next_instr()

@run_stats
def run(info_flag=0):
    initialize_run()

    while not done():
        display_info(info_flag)
        step()
