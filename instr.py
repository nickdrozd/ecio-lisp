'''
    TODO:
        * figure out a better way to resolve circular imports
'''

from reg import fetch, assign, CONT
from stack import clear_stack

from switch import switch
from labels import DONE, EVAL_EXP

from stats import goto_stats

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

def initialize_cont():
    assign(CONT, DONE)

def initialize():
    clear_stack()
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

def run():
    initialize()
    while not done():
        display_info()
        step()
